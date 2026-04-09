#!/usr/bin/env python3
"""测试动作建议功能"""

import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.api.action_suggestion import action_suggestion_generator

# 测试数据
test_company_profile = {
    "company_name": "深圳创新科技有限公司",
    "products_services": ["智能传感器", "物联网解决方案", "工业自动化设备"],
    "target_markets": ["北美", "欧洲"]
}

test_customer_strategy = {
    "recommended_markets": ["美国", "德国", "英国"],
    "recommended_segments": ["制造业", "医疗设备", "汽车配件"]
}

test_graded_customers = [
    {
        "company_name": "ABC Manufacturing Inc.",
        "location": "美国",
        "industry": "制造业",
        "website": "https://abc-manufacturing.example.com",
        "grade": "A",
        "total_score": 92.5
    },
    {
        "company_name": "XYZ Automotive GmbH",
        "location": "德国",
        "industry": "汽车配件",
        "website": "https://xyz-automotive.example.com",
        "grade": "B",
        "total_score": 78.0
    },
    {
        "company_name": "DEF Services Ltd.",
        "location": "英国",
        "industry": "咨询服务",
        "website": "https://def-services.example.com",
        "grade": "C",
        "total_score": 55.5
    },
    {
        "company_name": "GHI Retail Corp",
        "location": "日本",
        "industry": "零售",
        "website": "",
        "grade": "D",
        "total_score": 30.0
    }
]

def test_action_suggestion():
    print("=" * 60)
    print("测试动作建议功能")
    print("=" * 60)
    
    try:
        # 生成动作建议
        suggestions = action_suggestion_generator.generate_suggestions(
            test_graded_customers,
            test_company_profile,
            test_customer_strategy
        )
        
        print(f"\n✓ 成功生成 {len(suggestions)} 个客户的动作建议\n")
        
        # 打印每个客户的建议
        for i, suggestion in enumerate(suggestions, 1):
            print(f"\n{'=' * 60}")
            print(f"客户 {i}: {suggestion['customer_name']} (等级: {suggestion['grade']})")
            print(f"{'=' * 60}")
            print(f"优先级: {suggestion['priority']}")
            print(f"\n建议动作: {suggestion['suggested_action']}")
            print(f"\n建议渠道:")
            for channel in suggestion['suggested_channel']:
                print(f"  - {channel}")
            print(f"\n建议时机: {suggestion['suggested_timing']}")
            print(f"\n需要人工接管: {'是' if suggestion['needs_human_intervention'] else '否'}")
            print(f"\n开场话术:")
            print("-" * 60)
            print(suggestion['opening_script'])
            print("-" * 60)
        
        print("\n" + "=" * 60)
        print("✓ 所有测试通过！")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_action_suggestion()
    sys.exit(0 if success else 1)
