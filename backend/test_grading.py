#!/usr/bin/env python3
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.api.customer_grading import customer_grader

def test_customer_grading():
    print("=" * 60)
    print("测试客户分级功能")
    print("=" * 60)
    
    test_company_profile = {
        "company_name": "Test Manufacturing Co.",
        "industry": "Manufacturing",
        "products_services": ["Electronics", "Components", "PCB"],
        "target_markets": ["United States", "Germany", "Japan"],
        "key_strengths": ["Quality", "Innovation"]
    }
    
    test_customer_strategy = {
        "recommended_markets": ["United States", "Germany", "United Kingdom"],
        "recommended_segments": ["Technology", "Electronics", "Manufacturing"],
        "avoid_segments": [],
        "icp_lite": {
            "company_size": "medium to large",
            "industry": "Electronics",
            "location": "North America or Europe",
            "annual_spending": "待确认",
            "key_decision_makers": [],
            "pain_points": []
        },
        "missing_fields": []
    }
    
    test_customers = [
        {
            "company_name": "Global Tech Innovations Inc",
            "industry": "Technology",
            "location": "United States",
            "website": "https://globaltech.com",
            "source": "Mock Directory",
            "source_url": "https://mock-directory.com/search"
        },
        {
            "company_name": "European Electronics Ltd",
            "industry": "Electronics",
            "location": "Germany",
            "website": "https://europeanelectronics.de",
            "source": "Mock Directory",
            "source_url": "https://mock-directory.com/search"
        },
        {
            "company_name": "Local Workshop Studio",
            "industry": "Design",
            "location": "Brazil",
            "website": "",
            "source": "Mock Directory",
            "source_url": "https://mock-directory.com/search"
        }
    ]
    
    print("\n测试数据准备完成，开始分级...\n")
    
    try:
        graded_customers = customer_grader.grade_multiple_customers(
            test_customers,
            test_company_profile,
            test_customer_strategy
        )
        
        print(f"成功分级 {len(graded_customers)} 个客户：\n")
        
        for idx, customer in enumerate(graded_customers, 1):
            print(f"{'=' * 60}")
            print(f"客户 {idx}: {customer['company_name']}")
            print(f"{'=' * 60}")
            print(f"等级: {customer['grade']}")
            print(f"总分: {customer['total_score']:.1f}/{customer['max_total_score']}")
            print(f"\n分级原因: {customer['grade_reason']}")
            
            print("\n分维度得分:")
            for dim in customer['dimension_scores']:
                print(f"  - {dim['name']}: {dim['score']}/{dim['max_score']} ({dim['percentage']}%) - {dim['reason']}")
            
            print("\n关键依据:")
            for evidence in customer['key_evidences']:
                print(f"  - {evidence}")
            
            print("\n待核实项:")
            for verify in customer['to_verify']:
                print(f"  - {verify}")
            
            print()
        
        print("\n" + "=" * 60)
        print("测试成功！客户分级功能正常工作。")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_customer_grading()
    sys.exit(0 if success else 1)
