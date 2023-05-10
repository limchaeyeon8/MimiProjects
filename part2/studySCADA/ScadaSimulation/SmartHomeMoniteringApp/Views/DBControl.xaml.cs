using MahApps.Metro.Controls;
using MySql.Data.MySqlClient;
using Newtonsoft.Json;
using SmartHomeMonitoringApp.Logics;
using System;
using System.Collections.Generic;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using uPLibrary.Networking.M2Mqtt.Messages;

namespace SmartHomeMonitoringApp.Views
{
    /// <summary>
    /// DataBaseControl.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class DBControl : UserControl
    {
        public bool IsConnected { get; set; }

        ThreadStaticAttribute MqttThread { get; set; }      // 이 MQTT스레드 없으면 UI 컨트롤이 어려워짐

        public DBControl()
        {
            InitializeComponent();
        }



        // 유저 컨트롤 로드 이벤트 핸들러
        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {
            TxtBrokerUrl.Text = Commons.BROKERHOST;
            TxtMqttTopic.Text = Commons.MQTTTOPIC;
            TxtConnString.Text = Commons.MYSQL_CONNSTRING;

            IsConnected = false;        // 아직 접속이 안되었음
            BtnConnDb.IsChecked = false;

            // 실시간 모니터링에서 넘어왔을 때
            if (Commons.MQTT_CLIENT != null && Commons.MQTT_CLIENT.IsConnected)
            {
                IsConnected = true;
                BtnConnDb.IsChecked = true;

                Commons.MQTT_CLIENT.MqttMsgPublishReceived -= MQTT_CLIENT_MqttMsgPublishReceived;
            }
        }

        // 토글버튼 클릭이벤트 핸들러
        private void BtnConnDb_Click(object sender, RoutedEventArgs e)
        {
           ConnectDB();
        }

        private void ConnectDB()
        {
            if (IsConnected == false)
            {
                //MQTT 브로커에 접속
                Commons.MQTT_CLIENT = new uPLibrary.Networking.M2Mqtt.MqttClient(Commons.BROKERHOST);

                try
                {
                    // MQTT Subscribe (구독할) 로직
                    if (Commons.MQTT_CLIENT.IsConnected == false)
                    {
                        //MQTT 접속
                        Commons.MQTT_CLIENT.MqttMsgPublishReceived += MQTT_CLIENT_MqttMsgPublishReceived;
                        Commons.MQTT_CLIENT.Connect("MONITOR"); // ClientId = 모니터
                        Commons.MQTT_CLIENT.Subscribe(new string[] { Commons.MQTTTOPIC },
                            new byte[] { MqttMsgBase.QOS_LEVEL_AT_LEAST_ONCE });            // QOS는 네트워트 통신에 옵선
                        UpdateLog(">>> MQTT Broker Connected");

                        BtnConnDb.IsChecked = true;
                        BtnConnDb.Content = "MQTT 연결중";
                        IsConnected = true;     // 예외발생하면  true로 변경할 필요 없음
                    }
                }
                catch (Exception ex)
                {
                    UpdateLog($"!!! MQTT ERROR 발생 : {ex.Message}");
                }
            }
            else
            {

                try
                {
                    // 접속 중이라면 잠시 접속 끊어
                    if (Commons.MQTT_CLIENT.IsConnected == true)
                    {
                        Commons.MQTT_CLIENT.MqttMsgPublishReceived -= MQTT_CLIENT_MqttMsgPublishReceived;
                        Commons.MQTT_CLIENT.Disconnect();
                        UpdateLog(">>> MQTT Broker Disconnected...");

                        BtnConnDb.IsChecked = false;
                        BtnConnDb.Content = "MQTT 연결종료";
                        IsConnected = false;

                    }

                }
                catch (Exception ex)
                {
                    UpdateLog($"!!! MQTT ERROR 발생 : {ex.Message}");
                }

            }
        }

        private void UpdateLog(string msg)
        {
            //예외처리 필요!
            this.Invoke(() =>
            {
                TxtLog.Text += $"{msg}\n";
                TxtLog.ScrollToEnd();
            });
        }

        // Subscribe가 발생할 때 이벤트핸들러
        private void MQTT_CLIENT_MqttMsgPublishReceived(object sender, uPLibrary.Networking.M2Mqtt.Messages.MqttMsgPublishEventArgs e)
        {
            var msg = Encoding.UTF8.GetString(e.Message);
            UpdateLog(msg);
            SetToDataBase(msg, e.Topic); // 실제 DB에 저장처리
        }

        // DB 저장처리 메서드
        private void SetToDataBase(string msg, string topic)
        {
            var currValue = JsonConvert.DeserializeObject<Dictionary<string, string>>(msg);
            if (currValue != null)
            {
                //Debug.WriteLine(currValue["Home_Id"]);
                //Debug.WriteLine(currValue["Room_Name"]);
                //Debug.WriteLine(currValue["Sensing_DateTime"]);
                //Debug.WriteLine(currValue["Temp"]);
                //Debug.WriteLine(currValue["Humid"]);
                try
                {
                    using (MySqlConnection conn = new MySqlConnection(Commons.MYSQL_CONNSTRING))
                    {
                        if (conn.State == System.Data.ConnectionState.Closed) conn.Open();
                        string insQuery = @"INSERT INTO smarthomesensor
                                             (Home_Id,
                                              Room_Name,
                                              Sensing_DateTime,
                                              Temp,
                                              Humid)
                                            VALUES
                                             (@Home_Id,
                                              @Room_Name,
                                              @Sensing_DateTime,
                                              @Temp,
                                              @Humid)";

                        MySqlCommand cmd = new MySqlCommand(insQuery, conn);
                        cmd.Parameters.AddWithValue("@Home_Id", currValue["Home_Id"]);
                        cmd.Parameters.AddWithValue("@Room_Name", currValue["Room_Name"]);
                        cmd.Parameters.AddWithValue("@Sensing_DateTime", currValue["Sensing_DateTime"]);
                        cmd.Parameters.AddWithValue("@Temp", currValue["Temp"]);
                        cmd.Parameters.AddWithValue("@Humid", currValue["Humid"]);

                        if (cmd.ExecuteNonQuery() == 1)
                        {
                            UpdateLog(">>> DB Insert Succeed");
                        }
                        else
                        {
                            UpdateLog(">>> DB Insert Failed");  // 일어날 일 거의 없음
                        }
                    }
                }
                catch (Exception ex)
                {
                    UpdateLog($"!!! DB ERROR 발생 : {ex.Message}");
                }
            }
        }
    }
}