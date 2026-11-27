"""Adapter for upstream StanfordHCI/genagents (MIT).
Install and configure the upstream repository before using this adapter.
No network calls are made until simulate is explicitly invoked.
"""
def simulate(observations, scenario, choices, *, consent=False):
    if not consent:
        raise PermissionError("Harici model kullanımına açık onay gerekiyor.")
    if not observations or not scenario.strip() or len(choices) < 2:
        raise ValueError("Gözlemler, senaryo ve en az iki seçenek gerekli.")
    from genagents.genagents import GenerativeAgent
    agent = GenerativeAgent()
    for step, observation in enumerate(observations, 1):
        agent.remember(str(observation), time_step=step)
    result = agent.categorical_resp({scenario: list(choices)})
    return {"simulation": result, "validated_probability": None,
            "warning": "Simülasyon çıktısıdır; gerçek kişinin davranış garantisi değildir."}
