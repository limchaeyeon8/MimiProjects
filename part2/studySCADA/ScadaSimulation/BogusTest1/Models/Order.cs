using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BogusTest1.Models
{
    public class Order                              // 주문 테이블
    {
        public Guid Id { get; set; }                // 키값
        public DateTime Date { get; set; }          // 주문 일자
        public decimal OrderValue { get; set; }     // 주문 갯수
        public bool Shipped { get; set; }           // 선적 여부
    }
}
