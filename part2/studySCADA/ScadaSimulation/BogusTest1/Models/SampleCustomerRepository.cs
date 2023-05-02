using Bogus;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BogusTest1.Models
{
    public class SampleCustomerRepository
    {
        public IEnumerable<Customer> GetCustomers(int genNum)
        {
            /* IEnumerable 없으면 이렇게 해야 함
            var list = new List<Customer>();
            list.Add(new Customer 
            {
                Id = Guid.NewGuid(),
                Name = "임채연",
                Address = "부산",
                ...
            });
            var list = new List<Customer>();
            list.Add(new Customer
            {
                Id = Guid.NewGuid(),
                Name = "연채임",
                Address = "삱부",
                ...
            });
            ...*/

            Randomizer.Seed = new Random(123456);           // Seed 갯수를 지정 // 123456은 내맘대로
            // 아래와 같은 "규칙"으로 주문 더미데이터를 생성
            var orderGen = new Faker<Order>()
                .RuleFor(o => o.Id, Guid.NewGuid)           // Id값은 Guid로 자동생성()
                .RuleFor(o => o.Date, f => f.Date.Past(3))  // 날짜를 3년 전으로 세팅해서 생성
                .RuleFor(o => o.OrderValue, f => f.Finance.Amount(1, 10000)) // 1~10000까지 숫자중에서 랜덤하게 셋
                .RuleFor(o => o.Shipped, f => f.Random.Bool(0.8f));          // 0.5f라면 true/false가 반반

            // 고객 더미데이터 생성 규칙
            var customerGen = new Faker<Customer>()
                .RuleFor(c => c.Id, Guid.NewGuid)
                .RuleFor(c => c.Name, f => f.Company.CompanyName())     // 회사 이름 알아서 만들어줌
                .RuleFor(c => c.Address, f => f.Address.FullAddress())     // 가짜 주소 생성
                .RuleFor(c => c.Phone, f => f.Phone.PhoneNumber())
                .RuleFor(c => c.ContectName, f => f.Name.FullName())
                .RuleFor(c => c.Orders, f => orderGen.Generate(f.Random.Number(1, 2)).ToList());

            return customerGen.Generate(genNum);                 // 10개의 가짜 고객데이터를 생성, 리턴

        }

    }
}
