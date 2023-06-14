using BogusTestApp.Models;
using MahApps.Metro.Controls;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
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

namespace BogusTestApp
{
    /// <summary>
    /// MainWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class MainWindow : MetroWindow
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void BtnGenDummyData_Click(object sender, RoutedEventArgs e)
        {
            Random random = new Random();
            int a = random.Next(5);
            var repo = new SampleCustomerRepo();
            var customers = repo.GetCustomers(a);
            var result = JsonConvert.SerializeObject(customers, Formatting.Indented);
            TbxResult.Text =result;

        }
    }
}
