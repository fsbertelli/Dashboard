import requests
import csv
import threading
import time
from datetime import timedelta, timezone, datetime

robots = [
    1010, 1014, 1016, 1017, 1023, 1024, 1025, 1026, 1028, 1030, 1031, 1033,
    1041, 1042, 1043, 1044, 1046, 1047, 1049, 1050, 1051, 1055, 1060, 1061,
    1062, 1068, 1069, 1070, 1071, 1097, 1098
]

nome_arquivo = "/home/runner/solixdata/application/server/logs/robot_log.csv"

header = [
    "Date", "Time", "Robot","GPS_Status", "GPS_Speed", "Panel_Voltage", "Panel_Power",
    "Battery_Voltage","Remote_Control", "Battery_Power", "Electronic_Power", "Left_Power",
    "Right_Power", "Accessories_Power", "Last_Update"
]


def main():
  # Função para obter dados do robô e salvar em um arquivo CSV
  def get_and_save_robot_data(robot_id):
    while True:
      hora = timedelta(hours=-3)
      current_time = timezone(hora)
      data_hora_atual = datetime.now()
      hora_formatada = data_hora_atual.strftime("%H:%M:%S")
      data_atual = datetime.today()
      datef = data_atual.strftime("%d/%m/%Y")
      url = f'http://espia:strongpiopio042@52.161.96.125:3001/robot.log?{robot_id}'
      response = requests.get(url)

      if response.status_code == 200:
        data = response.text
        parts = data.split(',')

        if len(parts) >= 30:
          data_dict = {
              "Date": (datef),
              "Time": (hora_formatada),
              "Robot": str(robot_id),
              "GPS_Status": int(parts[1]),
              "GPS_Speed": str(parts[5]),
              "Panel_Voltage": round(float(parts[11]), 1),
              "Panel_Power": float(parts[13]),
              "Battery_Voltage": float(parts[12]),
              "Remote_Control": str(parts[15]),
              "Battery_Power": float(parts[16]),
              "Electronic_Power": float(parts[17]),
              "Left_Power": float(parts[18]),
              "Right_Power": float(parts[19]),
              "Accessories_Power": float(parts[27]),
              "Last_Update": int(parts[32]),
          }
          with open(nome_arquivo, mode='a', newline='') as arquivo_csv:
            escritor_csv = csv.writer(arquivo_csv,
                                      delimiter=';',
                                      quoting=csv.QUOTE_NONE)

            # Verifique se o arquivo está vazio e escreva o cabeçalho se for o caso
            if arquivo_csv.tell() == 0:
              escritor_csv.writerow(header)

            # Escreva os dados do dicionário em uma única linha
            linha = [data_dict[chave] for chave in header]
            escritor_csv.writerow(linha)

      time.sleep(1)  # Aguarde 60 segundos antes da próxima captura
      return hora_formatada

  # Função para realizar a captura de logs em paralelo
  def capture_logs_parallel():
    threads = []
    for robot in robots:
      thread = threading.Thread(target=get_and_save_robot_data, args=(robot, ))
      threads.append(thread)
      thread.start()

    for thread in threads:
      thread.join()

  while True:
    capture_logs_parallel()


if __name__ == "__main__":
  # Execute a função de captura de logs em paralelo
  print(f'Starting logging --> Streamlit must be started')
  main()
