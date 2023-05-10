using MahApps.Metro.Controls;
using Newtonsoft.Json;
using SmartHomeMonitoringApp.Logics;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using uPLibrary.Networking.M2Mqtt.Messages;

namespace SmartHomeMonitoringApp
{
    /// <summary>
    /// RealTimeControl.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class RealTimeControl : UserControl
    {
        public RealTimeControl()
        {
            InitializeComponent();

            // 머든 차트초기값
            LvcLivingTemp.Value = LvcDiningTemp.Value = LvcTemp.Value = LvcBath.Value = 0;
            LvcLivingTemp.Value = LvcDiningTemp.Value = LvcTemp.Value = LvcBath.Value = 0;
        }

        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {
            if (Commons.MQTT_CLIENT != null && Commons.MQTT_CLIENT.IsConnected)
            {
                // DB 모니터링을 실행한 뒤 실시간 모니터링을 넘어왔다면
                Commons.MQTT_CLIENT.MqttMsgPublishReceived += MQTT_CLIENT_MqttMsgPublishReceived;
            }
            else
            {
                // DB 모니터링을 실행하지 않고 실시간 모니터링을 넘어왔다면
            }
        }

        // MQTT Client는 단독스레드 사용 => UI스레드에 직접 접근 불가
        // this.Invoke(() => {} )  ---- UI스레드 안에 있는 리소스 접근 가능
        private void MQTT_CLIENT_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
        {
            var msg = Encoding.UTF8.GetString(e.Message);
            Debug.WriteLine(msg);
            var currSensor = JsonConvert.DeserializeObject<Dictionary<string, string>>(msg);

            if (currSensor["Home_Id"]=="D101H703")      // D101H703은 사용자 DB에서 동적으로 가져와야 할 값
            {
                this.Invoke(() =>
                {
                    var dfValue = DateTime.Parse(currSensor["Sensing_DateTime"].ToString("yyyy-MM-dd HH:mm:ss");
                    LblSensingDt.Content = $"Sensing DateTime : {dfValue}";
                });
                switch (currSensor["Room_Name"].ToUpper())        // 대문자
                {
                    case "LIVING":
                        this.Invoke(() =>       // UI스레드와의 충돌 방지
                        {
                            LvcLivingTemp.Value = Math.Round(Convert.ToDouble(currSensor["Temp"]));
                            LvcLivingHumid.Value = Math.Round(Convert.ToDouble(currSensor["Humid"]));
                        });
                        

                        break;

                    case "DINING":
                        this.Invoke(() =>       // UI스레드와의 충돌 방지
                        {
                            LvcDiningTemp.Value = Math.Round(Convert.ToDouble(currSensor["Temp"]));
                            LvcDiningHumid.Value = Math.Round(Convert.ToDouble(currSensor["Humid"]));
                        });
                        
                        break;

                    case "BED":
                        this.Invoke(() =>       // UI스레드와의 충돌 방지
                        {
                            LvcBedTemp.Value = Math.Round(Convert.ToDouble(currSensor["Temp"]));
                            LvcBedHumid.Value = Math.Round(Convert.ToDouble(currSensor["Humid"]));
                        });
                        
                        break;

                    case "BATH":
                        this.Invoke(() =>       // UI스레드와의 충돌 방지
                        {
                            LvcBathTemp.Value = Math.Round(Convert.ToDouble(currSensor["Temp"]));
                            LvcBathHumid.Value = Math.Round(Convert.ToDouble(currSensor["Humid"]));
                        });
                        
                        break;

                    default:
                        break;
                }
            }
        }
    }
}
