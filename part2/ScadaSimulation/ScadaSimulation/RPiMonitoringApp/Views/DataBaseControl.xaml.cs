using MahApps.Metro.Controls;
using MySql.Data.MySqlClient;
using Newtonsoft.Json;
using SmartHomeMonitoringApp.Logics;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Media.TextFormatting;
using System.Windows.Navigation;
using System.Windows.Shapes;
using uPLibrary.Networking.M2Mqtt.Messages;

namespace SmartHomeMonitoringApp.Views
{
    /// <summary>
    /// DataBaseControl.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class DataBaseControl : UserControl
    {
        public bool IsConnected { get; set; }
        Thread MqttThread { get; set; } // 없으면 UI 컨트롤이 어려워짐

        // MQTT Subscribtion text  과도 문제 속도 저하를 잡기위한 변수
        // 23.05.11 09:29 추가!
        int MaxCount { get; set; } = 10;

        public DataBaseControl()
        {
            InitializeComponent();
        }

        // 유저컨트롤 로드이벤트 핸들러
        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {
            TxbBrokerUrl.Text = Commons.BROKERHOST;
            TxbMqttTopic.Text = Commons.MQTTTOPIC;
            TxtConnString.Text = Commons.MYSQL_CONNSTRING;

            IsConnected = false;    // 아직 접속이 안됨.
            BtnConnDb.IsChecked = false;

            //실시간 모니터링에서 넘어왔을 때
            if(Commons.MQTT_CLIENT != null && Commons.MQTT_CLIENT.IsConnected)
            {
                IsConnected = true;
                BtnConnDb.IsChecked = true;
                Commons.MQTT_CLIENT.MqttMsgPublishReceived += MQTT_CLIENT_MqttMsgPublishReceived;
            }
        }

        // 토글버튼 클릭(1:접속/2:접속끊기) 이벤트 핸들러
        private void BtnConnDb_Click(object sender, RoutedEventArgs e)
        {
            ConnectDB();
        }

        private void ConnectDB()
        {
            if (IsConnected == false)
            {

                // Mqtt 브로커 생성
                Commons.MQTT_CLIENT = new uPLibrary.Networking.M2Mqtt.MqttClient(Commons.BROKERHOST);

                try
                {
                    // Mqtt subscribe 로직
                    if (Commons.MQTT_CLIENT.IsConnected == false)
                    {
                        // Mqtt 접속
                        Commons.MQTT_CLIENT.MqttMsgPublishReceived += MQTT_CLIENT_MqttMsgPublishReceived;
                        Commons.MQTT_CLIENT.Connect("MONITOR"); // clientId = 모니터
                        Commons.MQTT_CLIENT.Subscribe(new string[] { Commons.MQTTTOPIC },
                                new byte[] { MqttMsgBase.QOS_LEVEL_AT_LEAST_ONCE });    // QOS는 네트워크 통신 옵션
                        UpdateLog(">>> MQTT Broker Connected");

                        BtnConnDb.IsChecked = true;
                        BtnConnDb.Content = "MQTT 접속중";
                        IsConnected = true; // 예외발생하면 true
                    }
                }
                catch (Exception ex)
                {
                    UpdateLog($"!!! MQTT ERROR 발생 !!! : {ex.Message}");
                }
            }
            else
            {
                try
                {
                    if (Commons.MQTT_CLIENT.IsConnected)
                    {
                        Commons.MQTT_CLIENT.MqttMsgPublishReceived -= MQTT_CLIENT_MqttMsgPublishReceived;
                        Commons.MQTT_CLIENT.Disconnect();
                        UpdateLog(">>> MQTT Broker Disconnected!");

                        BtnConnDb.IsChecked = false;
                        BtnConnDb.Content = "MQTT 연결종료";
                        IsConnected = false;
                    }
                }
                catch (Exception ex)
                {
                    UpdateLog($"!!! MQTT ERROR 발생 !!! : {ex.Message}");

                }
            }
        }

        private void UpdateLog(string msg)
        {
            // 예외처리 필요
            this.Invoke(() =>
            {
                if(MaxCount <= 0)
                {
                    TxtLog.Text = string.Empty;
                    TxtLog.Text += ">>> 문서건수가 많아져 초기화!\n";
                    TxtLog.ScrollToEnd();
                    MaxCount = 10;  // 테스트 10, 운영 50
                }

                TxtLog.Text += $"{msg}\n";
                TxtLog.ScrollToEnd();
                MaxCount--;
            });
        }

        // Subscribe가 발생할 때 이벤트 핸들러
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
                Debug.WriteLine(currValue["DEV_ID"]);
                Debug.WriteLine(currValue["CURR_DT"]);
                Debug.WriteLine(currValue["TYPE"]);
                Debug.WriteLine(currValue["STAT"]);
                // Living
                var tmp = currValue["STAT"].Split('|');
                var temp = tmp[0].Trim();   // Trim 공백제거
                var humid = tmp[1].Trim();

                try
                {
                    using (MySqlConnection conn = new MySqlConnection(Commons.MYSQL_CONNSTRING))
                    {
                        if (conn.State == System.Data.ConnectionState.Closed) conn.Open();
                        string insQuery = @"INSERT INTO smarthomesensor
                                           (Home_id, Room_Name, Sensing_DateTime, Temp, Humid)
                                            VALUES  
                                           (@Home_id, @Room_Name, @Sensing_DateTime, @Temp, @Humid)";

                        MySqlCommand cmd = new MySqlCommand(insQuery, conn);
                        cmd.Parameters.AddWithValue("@Home_Id", currValue["DEV_ID"]);
                        cmd.Parameters.AddWithValue("@Room_Name", "Living");
                        cmd.Parameters.AddWithValue("@Sensing_DateTime", currValue["CURR_DT"]);
                        cmd.Parameters.AddWithValue("@Temp", temp);
                        cmd.Parameters.AddWithValue("@Humid", humid);

                        if (cmd.ExecuteNonQuery() == 1)
                        {
                            UpdateLog(">>> DB INSERT SUCCEED!");
                        }
                        else
                        {
                            UpdateLog(">>> DB INSERT FAILED!"); // 일어날 일 거의 없음
                        }
                    }

                }
                catch (Exception ex)
                {
                    UpdateLog($"!!! DB ERROR 발생 !!! : {ex.Message}");
                }
            }
        }
    }
}
