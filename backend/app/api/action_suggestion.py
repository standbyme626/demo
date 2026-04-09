from typing import Dict, Any, List, Optional


class ActionSuggestion:
    def __init__(self, customer: Dict[str, Any], company_profile: Dict[str, Any], customer_strategy: Dict[str, Any]):
        self.customer = customer
        self.company_profile = company_profile
        self.customer_strategy = customer_strategy
        self.grade = customer.get("grade", "D")
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "customer_name": self.customer.get("company_name", ""),
            "grade": self.grade,
            "suggested_action": self._get_suggested_action(),
            "suggested_channel": self._get_suggested_channel(),
            "suggested_timing": self._get_suggested_timing(),
            "opening_script": self._get_opening_script(),
            "needs_human_intervention": self._needs_human_intervention(),
            "priority": self._get_priority()
        }
    
    def _get_suggested_action(self) -> str:
        grade_actions = {
            "A": "立即重点跟进，约见决策人，准备定制化方案",
            "B": "积极跟进，发送产品资料和案例，安排初步沟通",
            "C": "适度跟进，先建立联系，发送产品目录",
            "D": "暂不投入，放入备选客户池，保持关注"
        }
        return grade_actions.get(self.grade, "暂不投入，放入备选客户池")
    
    def _get_suggested_channel(self) -> List[str]:
        grade_channels = {
            "A": ["Email + LinkedIn + 电话", "重点使用 LinkedIn 寻找决策人", "邮件发送定制化方案"],
            "B": ["Email + LinkedIn", "发送产品案例和资料", "LinkedIn 建立联系"],
            "C": ["Email", "发送产品目录和介绍", "官网联系表单"],
            "D": ["LinkedIn 关注", "订阅公司动态", "保持长期关注"]
        }
        return grade_channels.get(self.grade, ["LinkedIn 关注", "订阅公司动态"])
    
    def _get_suggested_timing(self) -> str:
        grade_timings = {
            "A": "24小时内完成初次联系，1周内安排深入沟通",
            "B": "3天内完成初次联系，2周内安排进一步沟通",
            "C": "1周内发送邮件，每月跟进一次",
            "D": "季度关注一次，不主动联系"
        }
        return grade_timings.get(self.grade, "季度关注一次，不主动联系")
    
    def _get_opening_script(self) -> str:
        company_name = self.customer.get("company_name", "贵公司")
        industry = self.customer.get("industry", "您所在的行业")
        location = self.customer.get("location", "您所在地区")
        company_products = ", ".join(self.company_profile.get("products_services", ["我们的产品"]))
        company_name_self = self.company_profile.get("company_name", "我们公司")
        
        grade_scripts = {
            "A": f"Hi [Name],\n\n我是{company_name_self}的[Your Name]。注意到{company_name}在{location}的{industry}领域的出色表现，相信我们的{company_products}可以为贵公司带来显著价值。\n\n希望能有机会与您或贵公司相关负责人深入探讨合作机会。\n\n期待您的回复！\n\nBest,\n[Your Name]",
            "B": f"Hi [Name],\n\n我是{company_name_self}的[Your Name]。看到{company_name}在{industry}领域的发展，想分享一下我们在{company_products}方面的成功案例，也许能为贵公司提供一些新思路。\n\n方便的时候我们可以简单聊一聊吗？\n\nBest,\n[Your Name]",
            "C": f"Hi [Name],\n\n我是{company_name_self}的[Your Name]。注意到{company_name}，想简单介绍一下我们的{company_products}。\n\n如果贵公司在这方面有需求或感兴趣，欢迎随时联系我。\n\nBest,\n[Your Name]",
            "D": f"Hi [Name],\n\n我是{company_name_self}的[Your Name]。关注到{company_name}的发展，想保持联系。我们专注于{company_products}，如果未来有相关需求，欢迎随时交流。\n\nBest,\n[Your Name]"
        }
        return grade_scripts.get(self.grade, "")
    
    def _needs_human_intervention(self) -> bool:
        return self.grade in ["A", "B"]
    
    def _get_priority(self) -> str:
        grade_priority = {
            "A": "最高优先级",
            "B": "高优先级",
            "C": "中优先级",
            "D": "低优先级"
        }
        return grade_priority.get(self.grade, "低优先级")


class ActionSuggestionGenerator:
    def __init__(self):
        pass
    
    def generate_suggestions(
        self, 
        graded_customers: List[Dict[str, Any]], 
        company_profile: Dict[str, Any], 
        customer_strategy: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        suggestions = []
        for customer in graded_customers:
            suggestion = ActionSuggestion(customer, company_profile, customer_strategy)
            suggestions.append(suggestion.to_dict())
        return suggestions


action_suggestion_generator = ActionSuggestionGenerator()
