import cv2
import numpy as np
from ultralytics import YOLO
import requests
from pytube import YouTube
from collections import deque

# Carregar o modelo YOLOv8
model = YOLO("yolov8l.pt")  # ou o caminho para o seu modelo .pt

# Definir a classe de pessoas
classes = ['person'] 
# Definir cores para as classes
colors = [(0, 255, 0)]  

# URL do vídeo do YouTube
youtube_url = 'https://www.youtube.com/watch?v=qlPKwGtuPq0' 

# Parâmetros do limiar adaptativo
limiar = 0.5  # Inicializar o limiar aqui
limiar_base = 0.5
ajuste_limiar = 0.2
tamanho_historico = 50 
historico_deteccoes = deque(maxlen=tamanho_historico)

try:
    # Crie um objeto YouTube
    yt = YouTube(youtube_url)

    # Selecione a maior resolução disponível (vídeo apenas)
    video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

    # Obtenha a URL direta do vídeo
    video_url = video_stream.url  

    print(f"URL do Vídeo: {video_url}")

    # Abrir o stream de vídeo
    cap = cv2.VideoCapture(video_url)

    # Verificar se o stream foi aberto com sucesso
    if not cap.isOpened():
        raise IOError("Não foi possível abrir o stream de vídeo")

    # Obter as dimensões originais do vídeo
    largura_original = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    altura_original = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Dimensões Originais: {largura_original}x{altura_original}")

    # Loop principal para processar os frames do vídeo
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Fazer a inferência com o YOLOv8
        results = model(frame)

        # Obter as detecções 
        detections = []
        for r in results:  
            boxes = r.boxes 
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                conf = box.conf[0]
                cls = box.cls[0] 

                # Usar o limiar ajustado
                if conf > limiar: 
                    detections.append((int(x1), int(y1), int(x2), int(y2), int(cls), float(conf)))

        # Contar pessoas
        people_count = len(detections)

        # Adicionar a contagem atual ao histórico
        historico_deteccoes.append(people_count)

        # Calcular a média de detecções no histórico
        media_deteccoes = np.mean(historico_deteccoes)

        # Ajustar o limiar com base na média de detecções (corrigido)
        if media_deteccoes > 10:  # Ajuste este valor se necessário
            limiar = limiar_base + ajuste_limiar
        else:
            limiar = limiar_base - ajuste_limiar

        # Imprimir informações no console
        print(f"Pessoas detectadas: {people_count}, Limiar: {limiar:.2f}")

        # Criar uma cópia do frame para desenhar as caixas 
        frame_desenho = frame.copy()

        # Desenhar caixas delimitadoras e rótulos
        for detection in detections:
            x1, y1, x2, y2, cls, conf = detection

            # Verificar se a classe detectada está na lista de classes
            if cls < len(classes): 
                # Obter a cor correspondente à classe
                color = colors[cls] 

                cv2.rectangle(frame_desenho, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame_desenho, f'{classes[cls]} - {conf:.2f}', (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Mostrar o número de pessoas detectadas na janela
        cv2.putText(frame_desenho, f'Pessoas: {people_count}', (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Mostrar o frame com as detecções
        cv2.imshow('Detecção de Pessoas', frame_desenho)

        # Aguardar tecla 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()

except Exception as e:
    print(f"Erro ao processar a URL do YouTube: {e}")
