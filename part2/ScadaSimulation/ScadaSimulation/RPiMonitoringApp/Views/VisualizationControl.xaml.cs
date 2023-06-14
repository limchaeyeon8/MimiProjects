using MySql.Data.MySqlClient;
using SmartHomeMonitoringApp.Logics;
using SmartHomeMonitoringApp.Models;
using System;
using System.Collections.Generic;
using System.Data;
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
using OxyPlot;
using OxyPlot.Series;
using OxyPlot.Legends;
using Google.Protobuf.WellKnownTypes;

namespace SmartHomeMonitoringApp.Views
{
    /// <summary>
    /// VisualizationControl.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class VisualizationControl : UserControl
    {
        List<string> Divisions = null;

        string FirstSensingDate = string.Empty;

        private int TotalDataCount = 0; // 검색된 데이터 개수

        public VisualizationControl()
        {
            InitializeComponent();
        }

        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {
            // 룸 선택 콤보박스 초기화
            Divisions = new List<string> { "SELECT", "LIVING", "DINING", "BED", "BATH" };
            CboRoomName.ItemsSource = Divisions;
            CboRoomName.SelectedIndex = 0;


            // 검색시작일 날짜 - DB에서 제일 오래된 날짜를 가져와서 할당
            using (MySqlConnection conn = new MySqlConnection(Commons.MYSQL_CONNSTRING))
            {
                conn.Open();
                var dtQuery = @"SELECT F.Sensing_Date 
                                  FROM(
	                                SELECT date_format(Sensing_DateTime, '%Y-%m-%d') AS Sensing_Date
		                                FROM smarthomesensor
                                  ) AS F
                                 GROUP BY F.Sensing_Date
                                 ORDER BY F.Sensing_Date ASC limit 1";

                MySqlCommand cmd = new MySqlCommand(dtQuery, conn);
                var result = cmd.ExecuteScalar();
                Debug.WriteLine(result.ToString());
                FirstSensingDate = DtpStart.Text = result.ToString();
                // 검색 종료일 현재일로 할당
                DtpEnd.Text = DateTime.Now.ToString("yyyy-MM-dd");
            }
        }

        private async void BtnSearch_Click(object sender, RoutedEventArgs e)
        {
            bool IsValid = true;
            string errorMsg = string.Empty;
            DataSet ds = new DataSet(); // DB 상에 있던 센싱데이터 담는 데이터셋

            // 검색, 저장, 수정, 삭제 전 반드시 검증(Validation)
            if (CboRoomName.SelectedValue.ToString() == "SELECT")
            {
                IsValid = false;
                errorMsg += "방 구분을 선택하시오.\n";
            }

            // 검색 시작일이 최초보다 빠르면
            if (DateTime.Parse(DtpStart.Text) < DateTime.Parse(FirstSensingDate))
            {
                IsValid = false;
                errorMsg += $"검색 시작일은 {FirstSensingDate} 이후로 선택하시오.\n";
            }

            // 오늘 날짜 이후 검색
            if (DateTime.Parse(DtpEnd.Text) > DateTime.Now)
            {
                IsValid = false;
                errorMsg += $"검색 종료일은 오늘까지 가능합니다.\n";
            }

            // 검색 시작일이 검색 종료일보다 이후면
            if (DateTime.Parse(DtpStart.Text) > DateTime.Parse(DtpEnd.Text))
            {
                IsValid = false;
                errorMsg += $"검색 시작일이 검색 종료일보다 최신일 수 없습니다.\n";
            }

            if(IsValid == false)
            {
                await Commons.ShowCustomMessageAsync("검색", errorMsg);
                return;
            }

            TotalDataCount = 0;
            // 검색 시작!
            try
            {
                using (MySqlConnection conn = new MySqlConnection(Commons.MYSQL_CONNSTRING))
                {
                    conn.Open();
                    var searchQuery = @"SELECT id,
	                                           Home_id
                                               Room_Name,
                                               Sensing_DateTime,
                                               Temp,
                                               Humid
                                          FROM smarthomesensor
                                         WHERE UPPER(Room_Name) = @Room_Name
                                           AND DATE_FORMAT(Sensing_DateTime, '%Y-%m-%d') 
                                       BETWEEN @StartDate AND @EndDate";

                    MySqlCommand cmd = new MySqlCommand(searchQuery, conn);
                    cmd.Parameters.AddWithValue("@Room_Name", CboRoomName.SelectedValue.ToString());
                    cmd.Parameters.AddWithValue("@StartDate", DtpStart.Text);
                    cmd.Parameters.AddWithValue("@EndDate", DtpEnd.Text);
                    MySqlDataAdapter adapter = new MySqlDataAdapter(cmd);
                    adapter.Fill(ds, "smarthomesensor");

                    //MessageBox.Show(ds.Tables["smarthomesensor"].Rows.Count.ToString(), "TotalData");         // 데이터 개수 확인
                }

            }
            catch (Exception ex)
            {
                await Commons.ShowCustomMessageAsync("DB검색", $"DB검색 오류 {ex.Message}");
            }

            // DB에서 가져온 데이터 차트에 뿌리도록 처리
            if (ds.Tables[0].Rows.Count >= 0)
            {
                TotalDataCount = ds.Tables[0].Rows.Count;

                // 선택한 방의 이름이 타이틀로 나오도록( Create the plot model )
                var tmp = new PlotModel { Title = $"{CboRoomName.SelectedValue} ROOM", DefaultFont = "Arial" };
                var lengend = new Legend
                {
                    LegendBorder = OxyColors.DarkGray,
                    LegendBackground = OxyColor.FromArgb(150, 255, 255, 255),
                    LegendPosition = LegendPosition.TopRight,
                    LegendPlacement = LegendPlacement.Outside
                };
                tmp.Legends.Add(lengend);

                // Create two line series (markers are hidden by default)
                var tempSeries = new LineSeries 
                { 
                    Title = "Temperature(℃)", // 타이틀 선정
                    MarkerType = MarkerType.Circle, // 마크 타입 선정
                    Color = OxyColors.DarkRed, // 라인 색상 선정
                };
                var humidSeries = new LineSeries 
                { 
                    Title = "Humidity(%),", 
                    MarkerType = MarkerType.Square,
                    Color = OxyColors.Cyan,
                };
                var count = 0;

                foreach (DataRow row in ds.Tables[0].Rows)
                {
                    tempSeries.Points.Add(new DataPoint(count++, Convert.ToDouble(row["Temp"])));
                    humidSeries.Points.Add(new DataPoint(count++, Convert.ToDouble(row["Humid"])));
                }

                // Add the series to the plot model
                tmp.Series.Add(tempSeries);
                tmp.Series.Add(humidSeries);
            
                OpvSmartHome.Model = tmp;

            }

            LblTotalCount.Content = $"검색데이터 {TotalDataCount}개";
        }
    }
}
