import requests
import base64

# URL do Worker AI da Cloudflare
API_URL = "https://api.cloudflare.com/client/v4/accounts/4cf5742c09485d76573a08baa743d7c6/ai/run/@cf/black-forest-labs/flux-1-schnell"

# Substitua pela sua chave de API (se necessário)
HEADERS = {
    "Authorization": "Bearer gYd0kUmnHN9RiMonmzXMSH9c--Yih5CgVrTs8FGj",
    "Content-Type": "application/json"
}

# Prompt para gerar a imagem
DATA = {
    "prompt": "An ultra-high-resolution, awe-inspiring depiction of Jesus Christ entrusting the keys of the Kingdom to the Apostle Peter, faithfully based on Matthew 16:18-19. Jesus stands in divine majesty, wearing a radiant white robe, His face filled with wisdom and authority. With a solemn and loving expression, He extends His hand, placing two large, golden keys into Peter’s hands—symbols of the authority to bind and loose on Earth and in Heaven. Peter, humbled and reverent, kneels before the Lord, his eyes filled with devotion and responsibility. The other apostles stand nearby, witnessing this sacred moment with a mix of awe and understanding. The setting is ancient Caesarea Philippi, with rolling hills and a serene sky bathed in warm, divine light, symbolizing the presence of the Holy Spirit. The composition is highly detailed, capturing the significance of this pivotal moment in Christian history with realism, sacred reverence, and artistic grandeur.",
    "width": 1024,
    "height": 1024,
    "num_inference_steps": 30
}

# Faz a requisição para gerar a imagem
response = requests.post(API_URL, json=DATA, headers=HEADERS)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    result = response.json()
    
    image_base64 = result["result"]["image"]
    
    if image_base64:
        # Converte Base64 para imagem
        try:
            with open("output.png", "wb") as img_file:
                img_file.write(base64.b64decode(image_base64))
            print("Imagem salva como output.png")
        except Exception as e:
            print(f"Erro ao decodificar a imagem: {e}")
else:
    print(f"Erro: {response.status_code}, {response.text}")