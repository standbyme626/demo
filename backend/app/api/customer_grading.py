from typing import Dict, Any, List, Optional
import openai
from app.config.config import settings

openai.api_key = settings.OPENAI_API_KEY

class DimensionScore:
    def __init__(self, name: str, score: float, max_score: float, reason: str):
        self.name = name
        self.score = score
        self.max_score = max_score
        self.reason = reason
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "score": self.score,
            "max_score": self.max_score,
            "percentage": round((self.score / self.max_score) * 100, 2),
            "reason": self.reason
        }

class GradedCustomer:
    def __init__(self, customer_data: Dict[str, Any]):
        self.customer_data = customer_data
        self.total_score = 0.0
        self.max_total_score = 100.0
        self.grade = ""
        self.dimension_scores: List[DimensionScore] = []
        self.grade_reason = ""
        self.key_evidences: List[str] = []
        self.to_verify: List[str] = []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **self.customer_data,
            "total_score": self.total_score,
            "max_total_score": self.max_total_score,
            "grade": self.grade,
            "dimension_scores": [ds.to_dict() for ds in self.dimension_scores],
            "grade_reason": self.grade_reason,
            "key_evidences": self.key_evidences,
            "to_verify": self.to_verify
        }

class CustomerGrader:
    def __init__(self):
        self.grade_intervals = {
            "S": (85, 100),
            "A": (70, 84),
            "B": (50, 69),
            "C": (30, 49),
            "D": (0, 29)
        }
        
        self.dimensions = [
            {"name": "公司类型匹配度", "max_score": 20},
            {"name": "采购规模匹配度", "max_score": 25},
            {"name": "决策人可触达性", "max_score": 20},
            {"name": "意图信号强度", "max_score": 20},
            {"name": "地域+认证匹配", "max_score": 15}
        ]
    
    def grade_customer(self, customer: Dict[str, Any], company_profile: Dict[str, Any], customer_strategy: Dict[str, Any]) -> GradedCustomer:
        graded_customer = GradedCustomer(customer)
        
        self._apply_rule_based_scoring(graded_customer, company_profile, customer_strategy)
        
        self._apply_model_based_enhancement(graded_customer, company_profile, customer_strategy)
        
        self._determine_grade(graded_customer)
        
        self._generate_explanation(graded_customer, company_profile, customer_strategy)
        
        return graded_customer
    
    def grade_multiple_customers(self, customers: List[Dict[str, Any]], company_profile: Dict[str, Any], customer_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        graded_customers = []
        for customer in customers:
            graded = self.grade_customer(customer, company_profile, customer_strategy)
            graded_customers.append(graded.to_dict())
        
        graded_customers.sort(key=lambda x: x["total_score"], reverse=True)
        return graded_customers
    
    def _apply_rule_based_scoring(self, graded_customer: GradedCustomer, company_profile: Dict[str, Any], customer_strategy: Dict[str, Any]):
        customer = graded_customer.customer_data
        
        company_type_score = self._score_company_type_match(customer, company_profile, customer_strategy)
        graded_customer.dimension_scores.append(company_type_score)
        
        procurement_size_score = self._score_procurement_size_match(customer, company_profile, customer_strategy)
        graded_customer.dimension_scores.append(procurement_size_score)
        
        decision_maker_access_score = self._score_decision_maker_accessibility(customer, company_profile, customer_strategy)
        graded_customer.dimension_scores.append(decision_maker_access_score)
        
        intent_signal_score = self._score_intent_signal_strength(customer, company_profile, customer_strategy)
        graded_customer.dimension_scores.append(intent_signal_score)
        
        region_certification_score = self._score_region_certification_match(customer, company_profile, customer_strategy)
        graded_customer.dimension_scores.append(region_certification_score)
        
        graded_customer.total_score = sum(ds.score for ds in graded_customer.dimension_scores)
    
    def _score_company_type_match(self, customer: Dict[str, Any], company_profile: Dict[str, Any], customer_strategy: Dict[str, Any]) -> DimensionScore:
        score = 0.0
        reason = ""
        customer_type = customer.get("customer_type", "").lower()
        recommended_segments = [s.lower() for s in customer_strategy.get("recommended_segments", [])]
        
        if any(segment in customer_type for segment in recommended_segments):
            score = 20.0
            reason = f"客户类型 '{customer.get('customer_type', '未知')}' 高度匹配推荐客群"
        elif customer_type:
            score = 12.0
            reason = f"客户类型 '{customer.get('customer_type', '未知')}' 基本匹配推荐客群"
        else:
            score = 5.0
            reason = "客户类型信息缺失，边缘匹配"
        
        return DimensionScore("公司类型匹配度", score, 20, reason)
    
    def _score_procurement_size_match(self, customer: Dict[str, Any], company_profile: Dict[str, Any], customer_strategy: Dict[str, Any]) -> DimensionScore:
        score = 0.0
        reason = ""
        
        company_name = customer.get("company_name", "").lower()
        size_indicators = {
            "large": ["group", "inc", "corporation", "global", "international", "holding"],
            "medium": ["ltd", "limited", "co.", "company"],
            "small": ["studio", "workshop", "local"]
        }
        
        detected_size = "unknown"
        for size, indicators in size_indicators.items():
            if any(indicator in company_name for indicator in indicators):
                detected_size = size
                break
        
        if detected_size == "large":
            score = 25.0
            reason = "客户规模较大，采购能力强，高度匹配"
        elif detected_size == "medium":
            score = 15.0
            reason = "客户规模中等，采购能力一般，基本匹配"
        else:
            score = 5.0
            reason = "客户规模较小，采购能力有限，过小或过大"
        
        return DimensionScore("采购规模匹配度", score, 25, reason)
    
    def _score_decision_maker_accessibility(self, customer: Dict[str, Any], company_profile: Dict[str, Any], customer_strategy: Dict[str, Any]) -> DimensionScore:
        score = 0.0
        reason = ""
        
        contact_name = customer.get("contact_name")
        contact_role = customer.get("contact_role")
        website = customer.get("website")
        
        if contact_name and contact_role:
            score = 20.0
            reason = "联系方式完整，职位明确，决策人可触达"
        elif website:
            score = 10.0
            reason = "有公司信息无联系人，可通过官网获取更多信息"
        else:
            score = 5.0
            reason = "仅官网信息，决策人触达难度较大"
        
        return DimensionScore("决策人可触达性", score, 20, reason)
    
    def _score_intent_signal_strength(self, customer: Dict[str, Any], company_profile: Dict[str, Any], customer_strategy: Dict[str, Any]) -> DimensionScore:
        score = 0.0
        reason = ""
        
        # 模拟意图信号检测
        website = customer.get("website", "").lower()
        company_name = customer.get("company_name", "").lower()
        
        signals = 0
        if "supplier" in website or "vendor" in website:
            signals += 1
        if "global" in website or "international" in website:
            signals += 1
        if "buy" in website or "purchase" in website:
            signals += 1
        
        if signals >= 2:
            score = 20.0
            reason = "2个以上强信号，采购意图明确"
        elif signals == 1:
            score = 12.0
            reason = "1个强信号，有一定采购意图"
        else:
            score = 5.0
            reason = "无明显采购信号"
        
        return DimensionScore("意图信号强度", score, 20, reason)
    
    def _score_region_certification_match(self, customer: Dict[str, Any], company_profile: Dict[str, Any], customer_strategy: Dict[str, Any]) -> DimensionScore:
        score = 0.0
        reason = ""
        
        customer_location = customer.get("location", "").lower()
        recommended_markets = [m.lower() for m in customer_strategy.get("recommended_markets", [])]
        
        # 假设公司有基本认证
        has_certification = True
        
        if customer_location in recommended_markets and has_certification:
            score = 15.0
            reason = "目标市场且有所需认证，匹配度高"
        elif customer_location in recommended_markets:
            score = 8.0
            reason = "市场匹配但无认证，匹配度一般"
        else:
            score = 3.0
            reason = "边缘市场，匹配度低"
        
        return DimensionScore("地域+认证匹配", score, 15, reason)
    
    def _determine_grade(self, graded_customer: GradedCustomer):
        score = graded_customer.total_score
        for grade, (min_score, max_score) in self.grade_intervals.items():
            if min_score <= score <= max_score:
                graded_customer.grade = grade
                break
    
    def _apply_model_based_enhancement(self, graded_customer: GradedCustomer, company_profile: Dict[str, Any], customer_strategy: Dict[str, Any]):
        pass
    
    def _generate_explanation(self, graded_customer: GradedCustomer, company_profile: Dict[str, Any], customer_strategy: Dict[str, Any]):
        grade = graded_customer.grade
        score = graded_customer.total_score
        
        grade_descriptions = {
            "S": "S级（本周冲刺），极高价值客户，建议立即重点跟进",
            "A": "A级（本周内首次触达），高价值客户，建议积极跟进",
            "B": "B级（本月内跟进），中等价值客户，可适度跟进",
            "C": "C级（长期维护），低价值客户，可长期维护",
            "D": "自动排除，无价值客户，建议排除"
        }
        
        graded_customer.grade_reason = f"客户综合得分为 {score:.1f} 分，评定为 {grade} 级。{grade_descriptions.get(grade, '')}"
        
        graded_customer.key_evidences = []
        for ds in graded_customer.dimension_scores:
            if ds.score >= ds.max_score * 0.8:
                graded_customer.key_evidences.append(f"{ds.name}: {ds.reason}")
        
        if not graded_customer.key_evidences:
            top_dimension = max(graded_customer.dimension_scores, key=lambda x: x.score)
            graded_customer.key_evidences.append(f"{top_dimension.name}: {top_dimension.reason}")
        
        graded_customer.to_verify = []
        customer = graded_customer.customer_data
        
        if not customer.get("location"):
            graded_customer.to_verify.append("核实客户具体地理位置")
        if not customer.get("industry"):
            graded_customer.to_verify.append("核实客户具体行业")
        if not customer.get("website"):
            graded_customer.to_verify.append("查找客户官方网站")
        graded_customer.to_verify.append("核实客户公司规模和年营收")
        graded_customer.to_verify.append("确认客户关键决策人联系方式")
        
        if not graded_customer.to_verify:
            graded_customer.to_verify.append("进一步了解客户具体采购需求")

customer_grader = CustomerGrader()
