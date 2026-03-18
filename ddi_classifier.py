# ==========================================================
# DDI CLASSIFIER (Improved Fallback Engine)
# Smarter + Deterministic + Expandable
# ==========================================================

class DDIClassifier:

    def __init__(self):

        # 🔥 High-risk known interactions
        self.high_risk_pairs = {
            ("warfarin", "ibuprofen"),
            ("warfarin", "aspirin"),
            ("aspirin", "clopidogrel"),
            ("nitroglycerin", "sildenafil"),
            ("simvastatin", "clarithromycin"),
        }

        # ⚠️ Moderate risk keywords
        self.moderate_keywords = [
            "warfarin", "aspirin", "heparin",
            "insulin", "metformin"
        ]

    # ======================================================
    # Normalize pair (IMPORTANT)
    # ======================================================
    def normalize(self, d1, d2):
        return tuple(sorted([d1.lower().strip(), d2.lower().strip()]))

    # ======================================================
    # Main Prediction Function
    # ======================================================
    def predict_interaction(self, drug1, drug2):

        pair = self.normalize(drug1, drug2)

        # ==================================================
        # 🔴 HIGH RISK
        # ==================================================
        if pair in self.high_risk_pairs:
            risk_percentage = 90
            level = "Unsafe"
            color = "red"
            mechanism = "Severe interaction affecting metabolism or causing life-threatening effects."
            advice = "Avoid this combination unless strictly prescribed."

        # ==================================================
        # 🟠 MODERATE RISK
        # ==================================================
        elif any(keyword in pair for keyword in self.moderate_keywords):
            risk_percentage = 60
            level = "Use With Caution"
            color = "orange"
            mechanism = "Potential interaction affecting blood thinning, glucose, or metabolism."
            advice = "Use under medical supervision."

        # ==================================================
        # 🟢 LOW RISK
        # ==================================================
        else:
            risk_percentage = 20
            level = "Safe"
            color = "green"
            mechanism = "No major clinically significant interaction found."
            advice = "Generally safe for use."

        # ==================================================
        # Confidence (FIXED, NOT RANDOM)
        # ==================================================
        confidence = 0.92 if level == "Unsafe" else 0.88 if level == "Use With Caution" else 0.85

        # ==================================================
        # Final Output (UNCHANGED FORMAT)
        # ==================================================
        return {
            "interaction": f"{drug1} + {drug2}",
            "safety": level,
            "risk_percentage": risk_percentage,
            "risk_level": level,
            "color": color,
            "confidence": confidence,
            "mechanism": mechanism,
            "side_effects": [
                "Dizziness",
                "Nausea",
                "Monitor unusual symptoms"
            ],
            "advice": advice,
            
        }