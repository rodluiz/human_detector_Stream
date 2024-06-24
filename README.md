Contador de Pessoas em Vídeos do YouTube com YOLOv8 e OpenCV
Este é um script Python que demonstra como usar o YOLOv8 para detecção de pessoas em tempo real em vídeos do YouTube, com exibição dos resultados usando OpenCV. O script inclui um mecanismo de ajuste de limiar dinâmico para lidar com variações no número de pessoas detectadas.
Recursos:
Baixa vídeos do YouTube via URL.
Realiza detecção de pessoas usando o modelo YOLOv8.
Desenha caixas delimitadoras ao redor das pessoas detectadas.
Exibe a contagem de pessoas em tempo real na janela de vídeo.
Implementa um limiar adaptativo para detecção, ajustando-se dinamicamente ao número de pessoas na cena.
Mostra a saída do vídeo processado usando OpenCV.
Pré-requisitos:
Python 3.7 ou superior
OpenCV (cv2)
Ultralytics YOLO (ultralytics)
PyTube (pytube)
NumPy (numpy)
Você pode instalar as bibliotecas necessárias usando o pip:
pip install opencv-python ultralytics pytube numpy
Use code with caution.
Bash
Como usar:
Baixe o modelo YOLOv8:
Baixe o modelo desejado (.pt) do Ultralytics YOLOv8 e coloque-o no mesmo diretório do script.
Insira a URL do YouTube:
Substitua 'https://www.youtube.com/watch?v=CWCVCTSb_ss' na variável youtube_url pela URL do vídeo do YouTube que você deseja processar.
Execute o script:
Execute o script Python.
O vídeo será baixado, processado e exibido em uma janela.
A contagem de pessoas e o limiar de detecção serão impressos no console.
Sair:
Pressione a tecla 'q' para sair do programa e fechar a janela de vídeo.
Notas:
O script está configurado para detectar apenas pessoas (classe 'person'). Você pode modificar a lista classes para detectar outras classes suportadas pelo YOLOv8.
A precisão e o desempenho do script dependem do modelo YOLOv8 escolhido. Modelos maiores e mais recentes geralmente oferecem melhor precisão, mas exigem mais recursos computacionais.
O limiar adaptativo ajuda a ajustar a sensibilidade da detecção com base na contagem de pessoas. Você pode ajustar os parâmetros limiar_base e ajuste_limiar para otimizar o desempenho de acordo com o vídeo de entrada.
Próximos Passos:
Integrar com outros sistemas, como enviar alertas quando a contagem de pessoas exceder um limite.
Implementar rastreamento de objetos para acompanhar indivíduos ao longo do tempo.
Criar uma interface gráfica do usuário (GUI) para facilitar o uso.
