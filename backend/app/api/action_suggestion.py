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
            "S": "本周冲刺，立即重点跟进，约见决策人，准备定制化方案",
            "A": "本周内首次触达，积极跟进，发送产品资料和案例，安排初步沟通",
            "B": "本月内跟进，适度跟进，先建立联系，发送产品目录",
            "C": "长期维护，保持联系，定期发送行业资讯",
            "D": "自动排除，无价值客户，建议排除"
        }
        return grade_actions.get(self.grade, "自动排除，无价值客户，建议排除")
    
    def _get_suggested_channel(self) -> List[str]:
        grade_channels = {
            "S": ["Email + LinkedIn + 电话 + 线下拜访", "重点使用 LinkedIn 寻找决策人", "邮件发送定制化方案"],
            "A": ["Email + LinkedIn + 电话", "发送产品案例和资料", "LinkedIn 建立联系"],
            "B": ["Email + LinkedIn", "发送产品目录和介绍", "官网联系表单"],
            "C": ["Email 定期发送", "LinkedIn 关注", "行业资讯分享"],
            "D": []
        }
        return grade_channels.get(self.grade, [])
    
    def _get_suggested_timing(self) -> str:
        grade_timings = {
            "S": "24小时内完成初次联系，3天内安排深入沟通，本周内完成冲刺",
            "A": "48小时内完成初次联系，1周内安排进一步沟通",
            "B": "1周内发送邮件，本月内完成跟进",
            "C": "每月跟进一次，长期维护",
            "D": "自动排除，无需跟进"
        }
        return grade_timings.get(self.grade, "自动排除，无需跟进")
    
    def _get_opening_script(self) -> str:
        company_name = self.customer.get("company_name", "贵公司")
        industry = self.customer.get("industry", "您所在的行业")
        location = self.customer.get("location", "您所在地区")
        company_products = ", ".join(self.company_profile.get("products_services", ["我们的产品"]))
        company_name_self = self.company_profile.get("company_name", "我们公司")
        
        grade_scripts = {
            "S": f"Hi [Name],\n\n我是{company_name_self}的[Your Name]。注意到{company_name}在{location}的{industry}领域的出色表现，相信我们的{company_products}可以为贵公司带来显著价值。\n\n我们本周正在重点跟进优质客户，希望能立即与您或贵公司相关负责人深入探讨合作机会。\n\n期待您的回复！\n\nBest,\n[Your Name]",
            "A": f"Hi [Name],\n\n我是{company_name_self}的[Your Name]。看到{company_name}在{industry}领域的发展，想分享一下我们在{company_products}方面的成功案例，也许能为贵公司提供一些新思路。\n\n希望本周内能与您安排一次初步沟通。\n\nBest,\n[Your Name]",
            "B": f"Hi [Name],\n\n我是{company_name_self}的[Your Name]。注意到{company_name}，想简单介绍一下我们的{company_products}。\n\n如果贵公司在这方面有需求或感兴趣，本月内我们可以安排一次交流。\n\nBest,\n[Your Name]",
            "C": f"Hi [Name],\n\n我是{company_name_self}的[Your Name]。关注到{company_name}的发展，想保持联系并定期分享行业资讯。\n\n我们专注于{company_products}，如果未来有相关需求，欢迎随时交流。\n\nBest,\n[Your Name]",
            "D": ""
        }
        return grade_scripts.get(self.grade, "")
    
    def _needs_human_intervention(self) -> bool:
        return self.grade in ["S", "A", "B"]
    
    def _get_priority(self) -> str:
        grade_priority = {
            "S": "本周冲刺 - 最高优先级",
            "A": "本周内 - 高优先级",
            "B": "本月内 - 中优先级",
            "C": "长期维护 - 低优先级",
            "D": "自动排除 - 无优先级"
        }
        return grade_priority.get(self.grade, "自动排除 - 无优先级")


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
