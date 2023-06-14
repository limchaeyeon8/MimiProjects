using MahApps.Metro.Controls;
using SmartHomeMonitoringApp.Logics;

namespace SmartHomeMonitoringApp.Views
{
    /// <summary>
    /// MqttPopupWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class MqttPopupWindow : MetroWindow
    {
        public MqttPopupWindow()
        {
            InitializeComponent();
        }

        // MQTT 접속 버튼 클릭이벤트 핸들러
        private void BtnConnect_Click(object sender, System.Windows.RoutedEventArgs e)
        {
            Commons.BROKERHOST = TxtBrokerIp.Text;
            Commons.MQTTTOPIC = TxtTopic.Text;

            this.DialogResult = true;
            this.Close();

        }

        //새 팝업로드 이벤트 핸들러
        private void MetroWindow_Loaded(object sender, System.Windows.RoutedEventArgs e)
        {
            TxtBrokerIp.Text = Commons.BROKERHOST;
            TxtTopic.Text = Commons.MQTTTOPIC;
        }
    }
}