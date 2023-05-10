using _1_FakeIotDevice.Models;
using Bogus;
using MahApps.Metro.Controls;
using MahApps.Metro.Controls.Dialogs;
using Newtonsoft.Json;
using System.Text;
using System.Diagnostics;
using System.Threading;
using System.Windows;
using uPLibrary.Networking.M2Mqtt;
using System.Windows.Documents;
using System;
using System.Security.AccessControl;

namespace _1_FakeIotDevice
{
    /// <summary>
    /// MainWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class MainWindow : MetroWindow
    {

        //
        Faker<SensorInfo> FakeHomeSensor = null;    // 가짜 스마트홈 센서값 변수

        MqttClient Client { get; set;}
        Thread MqttThread { get; set; }

        public MainWindow()
        {
            InitializeComponent();

            InitFakeData();                         // 전체(데이터 만들기) 초기화
        }

        private void InitFakeData()
        {
            var Rooms = new[] { "Bed", "Bath", "Living", "Dining" };

            FakeHomeSensor = new Faker<SensorInfo>()
                .RuleFor(s => s.Home_Id, "D101H1603")                       // 임의로 픽스된 스마트홈아이디
                .RuleFor(s => s.Room_Name, f => f.PickRandom(Rooms))        // PickRandom - 실행할 때마다 방이름이 계속 변경
                .RuleFor(s => s.Sensing_DateTime, f => f.Date.Past(0))      // 현재시각이 생성
                .RuleFor(s => s.Temp, f => f.Random.Float(20.0f, 30.0f))    // 20~30도 사이의 실수온도값 생성
                .RuleFor(s => s.Humid, f => f.Random.Float(40.0f, 64.0f));  // 40~64% 사이의 습도값 생성
        }

        private async void BtnConnect_Click(object sender, RoutedEventArgs e)
        {
            if (string.IsNullOrEmpty(TxtMqttBrokerIp.Text))
            {
                await this.ShowMessageAsync("오류", "브로커 아이피를 입력하세요♥");
                return;
            }


            // 브로커아이피로 접속
            ConnectMqttBroker();

            // 센싱은 끊어질 때까지 하위로직 무한반복
            StartPublish();

        }

        #region < 핵심처리 센싱된 데이터값을 MQTT 브로커로 전송 >
        private void StartPublish()
        {
            MqttThread = new Thread(() =>
            {
                while(true)
                {
                    // 가짜 스마트홈 센서값 생성
                    SensorInfo info = FakeHomeSensor.Generate();

                    // 릴리즈(배포) 때는 주석처리or삭제
                    Debug.WriteLine($"{info.Home_Id} | {info.Room_Name} | {info.Sensing_DateTime} | {info.Temp} | {info.Humid}");
                    // 객체 직렬화; 객체 데이터를 xml이나 json 등의 문자열로 변환
                    var jsonValue = JsonConvert.SerializeObject(info, Formatting.Indented);

                    // 센서값 MQTT브로커에 전송(Publish)
                    Client.Publish("SmartHome/IoTData/", Encoding.Default.GetBytes(jsonValue));        // 토픽 - 스마트홈에 개별적 집에 있는 IoT 데이터  // 이진바이트로 바꾸어 전달

                    // (+) 스레드-UI스레드 충돌이 안 나도록 변경
                    this.Invoke(new Action(() =>
                    {

                        // RtbLog에 출력
                        RtbLog.AppendText($"{jsonValue}\n");

                        RtbLog.ScrollToEnd();       // 스크롤 제일 밑으로 보내기
                    }));



                    // 1초동안 대기
                    Thread.Sleep(1000);
                }
            });
            MqttThread.Start();
        }

        private void ConnectMqttBroker()
        {
            Client = new MqttClient(TxtMqttBrokerIp.Text);
            Client.Connect("SmartHomeDev");         // publish하는 클라이언트 아이디 넣어줌(지정)
        }

        private async void MetroWindow_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            var mySetting = new MetroDialogSettings
            {
                AffirmativeButtonText = "끝내기",
                NegativeButtonText = "취소",
                AnimateShow = true,
                AnimateHide = true
            };

            var result = await this.ShowMessageAsync("프로그램 끝내기", "프로그램을 끝내시겠습니까?",
                MessageDialogStyle.AffirmativeAndNegative, mySetting);

            if (result == MessageDialogResult.Negative)
            {
                e.Cancel = true;
            }
            else
            {
                if (Commons.MQTT_CLIENT.IsConnected)
                {
                    Commons.MQTT_CLIENT.DisConnect;

                }
            }


            private void Btn 
        }

        #endregion
    }
}
