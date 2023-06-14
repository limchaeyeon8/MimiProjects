using Bogus;
using FakeIotDeviceApp.Models;
using MahApps.Metro.Controls;
using MahApps.Metro.Controls.Dialogs;
using Newtonsoft.Json;
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
using System.Windows.Navigation;
using System.Windows.Shapes;
using uPLibrary.Networking.M2Mqtt;

namespace FakeIotDeviceApp
{
    /// <summary>
    /// MainWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class MainWindow : MetroWindow
    {
        Faker<SensorInfo> FakeHomeSensor = null;    // 가짜 스마트홈 센서값 변수

        MqttClient Client;
        Thread MqttThread { get; set; }

        //MQTT Publish json 데이터 건수 체크 변수
        int MaxCount { get; set; } = 100;

        public MainWindow()
        {
            InitializeComponent();

            InitFakeData();
        }

        private void InitFakeData()
        {
            var Rooms = new[] { "Bed", "Bath", "Living", "Dining" };

            FakeHomeSensor = new Faker<SensorInfo>()
                .RuleFor(s => s.Home_Id, "D101H703")    // 임의로 픽스된 홈아이디
                .RuleFor(s => s.Room_Name, f => f.PickRandom(Rooms))    // 실행할 때마다 방이름이 계속 변경
                .RuleFor(s => s.Sensing_DateTime, f => f.Date.Past(0))  // 현재 시각이 생성
                .RuleFor(s => s.Temp, f => f.Random.Float(20.0f, 30.0f))  // 20~30 도 사이 온도값
                .RuleFor(s => s.Humid, f => f.Random.Float(40.0f, 64.0f));  // 40~64 사이 습도값
        }

        private async void BtnConnect_Click(object sender, RoutedEventArgs e)
        {
            if (string.IsNullOrEmpty(TxtMqttBrokerIP.Text))
            {
                await this.ShowMessageAsync("오류", "브로커아이피를 입력하세요");
                return;
            }

            // 브로커아이피로 접속
            ConnectMqttBroker();

            // 하위의 로직 무한 반복
            StartPublish();
        }

        private void StartPublish()
        {

            MqttThread = new Thread(() =>
            {
                while (true)
                {
                    // 가짜 스마트홈 센서값 생성
                    SensorInfo info = FakeHomeSensor.Generate();
                    // 디버그 -> 릴리즈 시 주석처리 필수!
                    Debug.WriteLine($"{info.Home_Id} / {info.Room_Name} / {info.Sensing_DateTime} / {info.Temp}");

                    // 객체 직렬화 (객체 데이터를 xml이나 json 등의 문자열로 만들어줌)
                    var jsonValue = JsonConvert.SerializeObject(info, Formatting.Indented);
                    // 센서값 MQTT브로커에 전송(Publish)
                    Client.Publish("SmartHome/IoTData/", Encoding.Default.GetBytes(jsonValue));
                    // 스레드와 UI 스레드 간 충돌이 안나도록 변경
                    this.Invoke(new Action(() =>
                    {
                        // RtbLog(RichTextBox)에 출력
                        RtbLog.AppendText($"Published : {jsonValue}\n");
                        RtbLog.ScrollToEnd();   // 스크롤 제일 밑으로 보내기
                        MaxCount--;
                        if( MaxCount <= 0)
                        {
                            RtbLog.SelectAll();
                            RtbLog.Selection.Text = string.Empty;
                            MaxCount = 50;
                            RtbLog.AppendText(">>> 문서건수가 많아져서 초기화.\n");
                        }
                    }));
                    
                    // 1초동안 대기
                    Thread.Sleep(1000);
                }
            });
            MqttThread.Start();
        }

        private void ConnectMqttBroker()
        {
            Client = new MqttClient(TxtMqttBrokerIP.Text);
            Client.Connect("SmartHomeDev"); //publish Client ID 지정
        }


        private void MetroWindow_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            if (Client.IsConnected == true)
            {
                Client.Disconnect();    // 접속 끊기
            }

            if(MqttThread != null)
            {
                MqttThread.Abort(); // 종료 후에 메모리에서도 삭제!
            }
        }
    }
} 
