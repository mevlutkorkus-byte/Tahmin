# Bilimsel kaynaklar

- StanfordHCI/genagents: https://github.com/StanfordHCI/genagents (MIT)
- Park ve diğerleri, Generative Agent Simulations of 1,000 People: https://arxiv.org/abs/2411.10109
- Centaur: https://huggingface.co/marcelbinz/Llama-3.1-Centaur-70B (ayrı lisans ve donanım değerlendirmesi gerekli)

GenAgents kaynak sınıfında GenerativeAgent(), remember(content, time_step) ve categorical_resp(questions) metotları doğrulandı. Mevcut adaptör bu API'yi çağırır. Upstream kurulum ve API yapılandırması henüz tamamlanmamıştır. Testler yalnızca yerel giriş ve onay kontrollerini kapsar; bilimsel tahmin doğruluğunu kanıtlamaz.
