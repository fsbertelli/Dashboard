import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

def creds_entered():
  if st.session_state["user"].strip() == "felipe.bertelli" and st.session_state["passwd"].strip() == "capoeirarosa":
      st.session_state["authenticated"] = True
      return True
  else:
      st.session_state["authenticated"] = False
      st.error("Você tem mesmo acesso? :face_with_raised_eyebrow:")
      return False

def autheticate_user():
  if "authenticated" not in st.session_state:
      st.text_input(label="Username: ", value="", key="user", on_change=creds_entered)
      st.text_input(label="Password: ", value="", key="passwd", type="password", on_change=creds_entered)
      return False
  else:
      if st.session_state["authenticated"]:
          return True
      else:
          st.text_input(label="Username: ", value="", key="user", on_change=creds_entered)
          st.text_input(label="Password: ", value="", key="passwd", type="password", on_change=creds_entered)    
          return False

if autheticate_user():
    st.set_page_config(
        page_title="Solix Dashboard",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items={
            'About': "felipe.bertelli@solinftec.com"
            }
        )
    st.sidebar.image("https://cdn-assets-cloud.frontify.com/s3/frontify-cloud-files-us/eyJwYXRoIjoiZnJvbnRpZnlcL2FjY291bnRzXC83Y1wvMjI0ODM4XC9wcm9qZWN0c1wvMzE1MTY0XC9hc3NldHNcLzA3XC81OTExMjMxXC84N2U1OTRjY2RjYzVlZjFiMzU3NDMxNDQ2YTQ2MjNkMC0xNjMzNTM1NDQ0LnBuZyJ9:frontify:_aMyS_Ee8qfVFoTmeHBn8PMo6UV9R5TO2wwiZoNO11c?width=2400", use_column_width="auto")
    st.sidebar.subheader('P&D - Grãos e Fibras')
    df = pd.read_csv("/home/runner/solixdata/application/server/logs/robot_log.csv", sep=";", decimal=".")
    df = df.sort_values(by="Robot")
    robot = st.sidebar.selectbox("Robôs", df["Robot"].unique())
    st.sidebar.caption('Report bugs: felipe.bertellI@solinftec.com')
    df_filtered = df[df["Robot"] == robot]
    #df_filtered 

    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S')
    df = df.sort_values(by='Time')
    df['Time'] = df['Time'].dt.strftime('%H:%M:%S')

    st.header(f"Robot {robot} Electronic Data")

    d = st.date_input("Selecione o Período", format="DD/MM/YYYY")
    date = d.strftime("%d/%m/%Y")
    df_sorted = df[(df["Date"] == date) & (df["Robot"] == robot)]
    df_filtered_date = df_sorted.sort_values(by="Time")

    mean_panel_voltage = df_filtered_date["Panel_Voltage"].mean()
    mean_panel_power = df_filtered_date["Panel_Power"].mean()
    mean_battery_voltage = df_filtered_date["Battery_Voltage"].mean()
    mean_battery_power = df_filtered_date["Battery_Power"].mean()
    mean_electronic_power = df_filtered_date["Electronic_Power"].mean()
    mean_acc_power = df_filtered_date["Accessories_Power"].mean()
    mean_left_power = df_filtered_date["Left_Power"].mean()
    mean_right_power = df_filtered_date["Right_Power"].mean()
    #------------------------------------------------------#
    max_panel_voltage = df_filtered_date["Panel_Voltage"].max()
    max_panel_power = df_filtered_date["Panel_Power"].max()
    max_battery_voltage = df_filtered_date["Battery_Voltage"].max()
    max_battery_power = df_filtered_date["Battery_Power"].max()
    max_electronic_power = df_filtered_date["Electronic_Power"].max()
    max_acc_power = df_filtered_date["Accessories_Power"].max()
    max_left_power = df_filtered_date["Left_Power"].max()
    max_right_power = df_filtered_date["Right_Power"].max()
    #------------------------------------------------------#
    min_panel_voltage = df_filtered_date["Panel_Voltage"].min()
    min_panel_power = df_filtered_date["Panel_Power"].min()
    min_battery_voltage = df_filtered_date["Battery_Voltage"].min()
    min_battery_power = df_filtered_date["Battery_Power"].min()
    min_electronic_power = df_filtered_date["Electronic_Power"].min()
    min_acc_power = df_filtered_date["Accessories_Power"].min()
    min_left_power = df_filtered_date["Left_Power"].min()
    min_right_power = df_filtered_date["Right_Power"].min()


    chart_type = st.selectbox("**Tipo de Gráfico**", ["Line", "Column", "Box", "Histogram", "Average Values"])
    mean_period = st.radio("Selecione o tipo de dados", 
            [":rainbow[Per Day]", ":rainbow[Per Mission]", ":rainbow[Daily DataFrame] :floppy_disk:", ":rainbow[Mission DataFrame] :floppy_disk:"], horizontal=True, disabled=False)
    if (df_filtered["Last_Update"] != 0).all():
      st.write(f':warning: Robô {robot} offline')
    

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)
    col7, col8 = st.columns(2)


    if df_filtered_date.empty:
      st.error("Não há dados para esse robô nesse período.")
    else:
      if mean_period == ":rainbow[Per Day]":
          match chart_type:
              case "Line":
                  fig_panel_voltage = px.line(df_filtered_date, x="Time", y="Panel_Voltage", 
                                              color="Robot", title="Panel Voltage", markers=False)
                  col1.plotly_chart(fig_panel_voltage)
                  col1.write(f"**🔝 Peak: {round(max_panel_voltage,2)}V**")
                  col1.write(f"**📊 Average: {round(mean_panel_voltage,2)}V**")
                  col1.write(f"**🆘 Min: {round(min_panel_voltage,2)}V**")


                  fig_panel_power = px.line(df_filtered_date, x="Time", y="Panel_Power",
                                          color="Robot", title="Panel Power", markers=False)
                  col2.plotly_chart(fig_panel_power)
                  col2.write(f"**🔝 Peak: {round(max_panel_power,2)}W**")
                  col2.write(f"**📊 Average: {round(mean_panel_power,2)}W**")
                  col2.write(f"**🆘 Min: {round(min_panel_power,2)}W**")

                  fig_battery_voltage = px.line(df_filtered_date, x="Time", y="Battery_Voltage", 
                                      color="Robot", title="Battery Voltage", markers=False)
                  col3.plotly_chart(fig_battery_voltage)
                  col3.write(f"**🔝 Peak: {round(max_battery_voltage,2)}V**")
                  col3.write(f"**📊 Average: {round(mean_battery_voltage,2)}V**")
                  col3.write(f"**🆘 Min: {round(min_battery_voltage,2)}V**")

                  fig_battery_power = px.line(df_filtered_date, x="Time", y="Battery_Power",
                                              color="Robot", title="Battery Power", markers=False)
                  col4.plotly_chart(fig_battery_power)
                  col4.write(f"**🔝 Peak: {round(max_battery_power,2)}W**")
                  col4.write(f"**📊 Average: {round(mean_battery_power,2)}W**")
                  col4.write(f"**🆘 Min: {round(min_battery_power,2)}W**")


                  fig_eletronic_power = px.line(df_filtered_date, x="Time", y="Electronic_Power",
                                              color="Robot", title="Eletronic Power", markers=False)
                  col5.plotly_chart(fig_eletronic_power)
                  col5.write(f"**🔝 Peak: {round(max_electronic_power,2)}W**")
                  col5.write(f"**📊 Average: {round(mean_electronic_power,2)}W**")
                  col5.write(f"**🆘 Min: {round(min_electronic_power,2)}W**")


                  fig_acc_power = px.line(df_filtered_date, x="Time", y="Accessories_Power",
                                          color="Robot", title="ACC Power", markers=False)
                  col6.plotly_chart(fig_acc_power)
                  col6.write(f"**🔝 Peak: {round(max_acc_power,2)}W**")
                  col6.write(f"**📊 Average: {round(mean_acc_power,2)}W**")
                  col6.write(f"**🆘 Min: {round(min_acc_power,2)}W**")


                  motor_left_power = px.line(df_filtered_date, x="Time", y="Left_Power",
                                          color="Robot", title="Left Power", markers=False)
                  col7.plotly_chart(motor_left_power)
                  col7.write(f"**🔝 Peak: {round(max_left_power,2)}W**")
                  col7.write(f"**📊 Average: {round(mean_left_power,2)}W**")
                  col7.write(f"**🆘 Min: {round(min_left_power,2)}W**")

                  motor_right_power = px.line(df_filtered_date, x="Time", y="Right_Power",
                                          color="Robot", title="Right Power", markers=False)
                  col8.plotly_chart(motor_right_power)
                  col8.write(f"**🔝 Peak: {round(max_right_power,2)}W**")
                  col8.write(f"**📊 Average: {round(mean_right_power,2)}W**")
                  col8.write(f"**🆘 Min: {round(min_right_power,2)}W**")
              case "Column":

                  fig_panel_voltage = px.bar(df_filtered_date, x="Time", y="Panel_Voltage", 
                                              color="Robot", title="Panel Voltage")
                  col1.plotly_chart(fig_panel_voltage)
                  col1.write(f"**🔝 Peak: {round(max_panel_voltage,2)}V**")
                  col1.write(f"**📊 Average: {round(mean_panel_voltage,2)}V**")
                  col1.write(f"**🆘 Min: {round(min_panel_voltage,2)}V**")  

                  fig_panel_power = px.bar(df_filtered_date, x="Time", y="Panel_Power",
                                          color="Robot", title="Panel Power")
                  col2.plotly_chart(fig_panel_power)
                  col2.write(f"**🔝 Peak: {round(max_panel_power,2)}W**")
                  col2.write(f"**📊 Average: {round(mean_panel_power,2)}W**")
                  col2.write(f"**🆘 Min: {round(min_panel_power,2)}W**")

                  fig_battery_voltage = px.bar(df_filtered_date, x="Time", y="Battery_Voltage", 
                                      color="Robot", title="Battery Voltage")
                  col3.plotly_chart(fig_battery_voltage)
                  col3.write(f"**🔝 Peak: {round(max_battery_voltage,2)}V**")
                  col3.write(f"**📊 Average: {round(mean_battery_voltage,2)}V**")
                  col3.write(f"**🆘 Min: {round(min_battery_voltage,2)}V**")

                  fig_battery_power = px.bar(df_filtered_date, x="Time", y="Battery_Power",
                                              color="Robot", title="Battery Power")
                  col4.plotly_chart(fig_battery_power)
                  col4.write(f"**🔝 Peak: {round(max_battery_power,2)}W**")
                  col4.write(f"**📊 Average: {round(mean_battery_power,2)}W**")
                  col4.write(f"**🆘 Min: {round(min_battery_power,2)}W**")

                  fig_eletronic_power = px.bar(df_filtered_date, x="Time", y="Electronic_Power",
                                              color="Robot", title="Eletronic Power")
                  col5.plotly_chart(fig_eletronic_power)
                  col5.write(f"**🔝 Peak: {round(max_electronic_power,2)}W**")
                  col5.write(f"**📊 Average: {round(mean_electronic_power,2)}W**")
                  col5.write(f"**🆘 Min: {round(min_electronic_power,2)}W**")


                  fig_acc_power = px.bar(df_filtered_date, x="Time", y="Accessories_Power",
                                          color="Robot", title="ACC Power")
                  col6.plotly_chart(fig_acc_power)
                  col6.write(f"**🔝 Peak: {round(max_acc_power,2)}W**")
                  col6.write(f"**📊 Average: {round(mean_acc_power,2)}W**")
                  col6.write(f"**🆘 Min: {round(min_acc_power,2)}W**")

                  motor_left_power = px.bar(df_filtered_date, x="Time", y="Left_Power",
                                          color="Robot", title="Left Power")
                  col7.plotly_chart(motor_left_power)
                  col7.write(f"**🔝 Peak: {round(max_left_power,2)}W**")
                  col7.write(f"**📊 Average: {round(mean_left_power,2)}W**")
                  col7.write(f"**🆘 Min: {round(min_left_power,2)}W**")

                  motor_right_power = px.bar(df_filtered_date, x="Time", y="Right_Power",
                                          color="Robot", title="Right Power")
                  col8.plotly_chart(motor_right_power)
                  col8.write(f"**🔝 Peak: {round(max_right_power,2)}W**")
                  col8.write(f"**📊 Average: {round(mean_right_power,2)}W**")
                  col8.write(f"**🆘 Min: {round(min_right_power,2)}W**")
              case "Box":
                  fig_panel_voltage = px.box(df_filtered_date, y="Panel_Voltage", 
                                              color="Robot", title="Panel Voltage")
                  col1.plotly_chart(fig_panel_voltage)
                  col1.write(f"**🔝 Peak: {round(max_panel_voltage,2)}V**")
                  col1.write(f"**📊 Average: {round(mean_panel_voltage,2)}V**")
                  col1.write(f"**🆘 Min: {round(min_panel_voltage,2)}V**")

                  fig_panel_power = px.box(df_filtered_date,  y="Panel_Power",
                                          color="Robot", title="Panel Power")
                  col2.plotly_chart(fig_panel_power)
                  col2.write(f"**🔝 Peak: {round(max_panel_power,2)}W**")
                  col2.write(f"**📊 Average: {round(mean_panel_power,2)}W**")
                  col2.write(f"**🆘 Min: {round(min_panel_power,2)}W**")

                  fig_battery_voltage = px.box(df_filtered_date,  y="Battery_Voltage", 
                                      color="Robot", title="Battery Voltage")
                  col3.plotly_chart(fig_battery_voltage)
                  col3.write(f"**🔝 Peak: {round(max_battery_voltage,2)}V**")
                  col3.write(f"**📊 Average: {round(mean_battery_voltage,2)}V**")
                  col3.write(f"**🆘 Min: {round(min_battery_voltage,2)}V**")

                  fig_battery_power = px.box(df_filtered_date,  y="Battery_Power",
                                              color="Robot", title="Battery Power")
                  col4.plotly_chart(fig_battery_power)
                  col4.write(f"**🔝 Peak: {round(max_battery_power,2)}W**")
                  col4.write(f"**📊 Average: {round(mean_battery_power,2)}W**")
                  col4.write(f"**🆘 Min: {round(min_battery_power,2)}W**")

                  fig_eletronic_power = px.box(df_filtered_date,  y="Electronic_Power",
                                              color="Robot", title="Eletronic Power")
                  col5.plotly_chart(fig_eletronic_power)
                  col5.write(f"**🔝 Peak: {round(max_electronic_power,2)}W**")
                  col5.write(f"**📊 Average: {round(mean_electronic_power,2)}W**")
                  col5.write(f"**🆘 Min: {round(min_electronic_power,2)}W**")

                  fig_acc_power = px.box(df_filtered_date,  y="Accessories_Power",
                                          color="Robot", title="ACC Power")
                  col6.plotly_chart(fig_acc_power)
                  col6.write(f"**🔝 Peak: {round(max_acc_power,2)}W**")
                  col6.write(f"**📊 Average: {round(mean_acc_power,2)}W**")
                  col6.write(f"**🆘 Min: {round(min_acc_power,2)}W**")

                  motor_left_power = px.box(df_filtered_date,  y="Left_Power",
                                          color="Robot", title="Left Power")
                  col7.plotly_chart(motor_left_power)
                  col7.write(f"**🔝 Peak: {round(max_left_power,2)}W**")
                  col7.write(f"**📊 Average: {round(mean_left_power,2)}W**")
                  col7.write(f"**🆘 Min: {round(min_left_power,2)}W**")

                  motor_right_power = px.box(df_filtered_date,  y="Right_Power",
                                          color="Robot", title="Right Power")
                  col8.plotly_chart(motor_right_power)
                  col8.write(f"**🔝 Peak: {round(max_right_power,2)}W**")
                  col8.write(f"**📊 Average: {round(mean_right_power,2)}W**")
                  col8.write(f"**🆘 Min: {round(min_right_power,2)}W**")
              case "Histogram":
                  fig_panel_voltage = px.histogram(df_filtered_date, x="Panel_Voltage", 
                                              color="Robot", title="Panel Voltage")
                  col1.plotly_chart(fig_panel_voltage)
                  col1.write(f"**🔝 Peak: {round(max_panel_voltage,2)}V**")
                  col1.write(f"**📊 Average: {round(mean_panel_voltage,2)}V**")
                  col1.write(f"**🆘 Min: {round(min_panel_voltage,2)}V**")


                  fig_panel_power = px.histogram(df_filtered_date,  x="Panel_Power",
                                          color="Robot", title="Panel Power")
                  col2.plotly_chart(fig_panel_power)
                  col2.write(f"**🔝 Peak: {round(max_panel_power,2)}W**")
                  col2.write(f"**📊 Average: {round(mean_panel_power,2)}W**")
                  col2.write(f"**🆘 Min: {round(min_panel_power,2)}W**")

                  fig_battery_voltage = px.histogram(df_filtered_date,  x="Battery_Voltage", 
                                      color="Robot", title="Battery Voltage")
                  col3.plotly_chart(fig_battery_voltage)
                  col3.write(f"**🔝 Peak: {round(max_battery_voltage,2)}V**")
                  col3.write(f"**📊 Average: {round(mean_battery_voltage,2)}V**")
                  col3.write(f"**🆘 Min: {round(min_battery_voltage,2)}V**")

                  fig_battery_power = px.histogram(df_filtered_date,  x="Battery_Power",
                                              color="Robot", title="Battery Power")
                  col4.plotly_chart(fig_battery_power)
                  col4.write(f"**🔝 Peak: {round(max_battery_power,2)}W**")
                  col4.write(f"**📊 Average: {round(mean_battery_power,2)}W**")
                  col4.write(f"**🆘 Min: {round(min_battery_power,2)}W**")


                  fig_eletronic_power = px.histogram(df_filtered_date,  x="Electronic_Power",
                                              color="Robot", title="Eletronic Power")
                  col5.plotly_chart(fig_eletronic_power)
                  col5.write(f"**🔝 Peak: {round(max_electronic_power,2)}W**")
                  col5.write(f"**📊 Average: {round(mean_electronic_power,2)}W**")
                  col5.write(f"**🆘 Min: {round(min_electronic_power,2)}W**")


                  fig_acc_power = px.histogram(df_filtered_date,  x="Accessories_Power",
                                          color="Robot", title="ACC Power")
                  col6.plotly_chart(fig_acc_power)
                  col6.write(f"**🔝 Peak: {round(max_acc_power,2)}W**")
                  col6.write(f"**📊 Average: {round(mean_acc_power,2)}W**")
                  col6.write(f"**🆘 Min: {round(min_acc_power,2)}W**")


                  motor_left_power = px.histogram(df_filtered_date,  x="Left_Power",
                                          color="Robot", title="Left Power")
                  col7.plotly_chart(motor_left_power)
                  col7.write(f"**🔝 Peak: {round(max_left_power,2)}W**")
                  col7.write(f"**📊 Average: {round(mean_left_power,2)}W**")
                  col7.write(f"**🆘 Min: {round(min_left_power,2)}W**")

                  motor_right_power = px.histogram(df_filtered_date,  x="Right_Power",
                                          color="Robot", title="Right Power")
                  col8.plotly_chart(motor_right_power)
                  col8.write(f"**🔝 Peak: {round(max_right_power,2)}W**")
                  col8.write(f"**📊 Average: {round(mean_right_power,2)}W**")
                  col8.write(f"**🆘 Min: {round(min_right_power,2)}W**")

              case "Average Values":  
                  col1.write(f"**Average Panel Voltage: {round(mean_panel_voltage,2)}V**")
                  col2.write(f"**Average Panel Power: {round(mean_panel_power,2)}W**")
                  col1.write(f"**Average Battery Voltage: {round(mean_battery_voltage,2)}V**")
                  col2.write(f"**Average Battery Power: {round(mean_panel_power,2)}W**")
                  col1.write(f"**Average Eletronic Power: {round(mean_electronic_power,2)}W**")
                  col2.write(f"**Average ACC Power: {round(mean_acc_power,2)}W**")
                  col1.write(f"**Average Left Motor Power: {round(mean_left_power,2)}W**")
                  col2.write(f"**Average Right Motor Power: {round(mean_right_power,2)}W**")
                  robot_consumption = round((mean_battery_power/mean_battery_voltage),2)
                  col1.write(f"**Average Robots Consumption: {robot_consumption}A**")
                  robot_generate = round((mean_panel_power/mean_panel_voltage),2)
                  col2.write(f"**Average Robots Generation: {robot_generate}A**")

                  fig_panel_voltage = px.line(df_filtered_date, x="Time", y="Panel_Voltage", color="Robot", title="Panel Voltage", markers=False)
                  fig_panel_voltage.add_shape(
                      go.layout.Shape(
                          type="line",
                          x0=df_filtered_date['Time'].min(),
                          x1=df_filtered_date['Time'].max(),
                          y0=mean_panel_voltage,
                          y1=mean_panel_voltage,
                          line=dict(color="red", width=2)
                      )
                  )
                  col1.plotly_chart(fig_panel_voltage)

                  fig_panel_power = px.line(df_filtered_date, x="Time", y="Panel_Power", color="Robot", title="Average Panel Power", markers=False)
                  fig_panel_power.add_shape(
                      go.layout.Shape(
                          type="line",
                          x0=df_filtered_date['Time'].min(),
                          x1=df_filtered_date['Time'].max(),
                          y0=mean_panel_power,
                          y1=mean_panel_power,
                          line=dict(color="red", width=2)
                      )
                  )
                  col2.plotly_chart(fig_panel_power)

                  fig_battery_voltage = px.line(df_filtered_date, x="Time", y="Battery_Voltage", color="Robot", title="Average Battery Voltage", markers=False)
                  fig_battery_voltage.add_shape(
                      go.layout.Shape(
                          type="line",
                          x0=df_filtered_date['Time'].min(),
                          x1=df_filtered_date['Time'].max(),
                          y0=mean_battery_voltage,
                          y1=mean_battery_voltage,
                          line=dict(color="red", width=2)
                      )
                  )
                  col3.plotly_chart(fig_battery_voltage)

                  fig_battery_power = px.line(df_filtered_date, x="Time", y="Battery_Power", color="Robot", title="Average Battery Power", markers=False)
                  fig_battery_power.add_shape(
                      go.layout.Shape(
                          type="line",
                          x0=df_filtered_date['Time'].min(),
                          x1=df_filtered_date['Time'].max(),
                          y0=mean_battery_power,
                          y1=mean_battery_power,
                          line=dict(color="red", width=2)
                      )
                  )
                  col4.plotly_chart(fig_battery_power)

                  fig_eletronic_power = px.line(df_filtered_date, x="Time", y="Electronic_Power", color="Robot", title="Average Electronic Power", markers=False)
                  fig_eletronic_power.add_shape(
                      go.layout.Shape(
                          type="line",
                          x0=df_filtered_date['Time'].min(),
                          x1=df_filtered_date['Time'].max(),
                          y0=mean_electronic_power,
                          y1=mean_electronic_power,
                          line=dict(color="red", width=2)
                      )
                  )
                  col5.plotly_chart(fig_eletronic_power)

                  fig_acc_power = px.line(df_filtered_date, x="Time", y="Accessories_Power", color="Robot", title="Average ACC Power", markers=False)
                  fig_acc_power.add_shape(
                      go.layout.Shape(
                          type="line",
                          x0=df_filtered_date['Time'].min(),
                          x1=df_filtered_date['Time'].max(),
                          y0=mean_acc_power,
                          y1=mean_acc_power,
                          line=dict(color="red", width=2)
                      )
                  )
                  col6.plotly_chart(fig_acc_power)

                  fig_left_power = px.line(df_filtered_date, x="Time", y="Left_Power", color="Robot", title="Average Motor Left Power", markers=False)
                  fig_left_power.add_shape(
                      go.layout.Shape(
                          type="line",
                          x0=df_filtered_date['Time'].min(),
                          x1=df_filtered_date['Time'].max(),
                          y0=mean_left_power,
                          y1=mean_left_power,
                          line=dict(color="red", width=2)
                      )
                  )
                  col7.plotly_chart(fig_left_power)

                  fig_right_power = px.line(df_filtered_date, x="Time", y="Right_Power", color="Robot", title="Average Motor Right Power", markers=False)
                  fig_right_power.add_shape(
                      go.layout.Shape(
                          type="line",
                          x0=df_filtered_date['Time'].min(),
                          x1=df_filtered_date['Time'].max(),
                          y0=mean_right_power,
                          y1=mean_right_power,
                          line=dict(color="red", width=2)
                      )
                  )
                  col8.plotly_chart(fig_right_power)

      elif mean_period == ":rainbow[Per Mission]":
        df_filtered_mission = df[
            (df["Date"] == date) &          
            (df["Robot"] == robot) &        
            (df["GPS_Speed"] > 0.5) &      
            (df["Last_Update"] == 0) &    
            (df["Remote_Control"] != 'RADIO') &
            (df["GPS_Status"] == 44)
        ]

        mean_panel_voltage = df_filtered_mission["Panel_Voltage"].mean()
        mean_panel_power = df_filtered_mission["Panel_Power"].mean()
        mean_battery_voltage = df_filtered_mission["Battery_Voltage"].mean()
        mean_battery_power = df_filtered_mission["Battery_Power"].mean()
        mean_electronic_power = df_filtered_mission["Electronic_Power"].mean()
        mean_acc_power = df_filtered_mission["Accessories_Power"].mean()
        mean_left_power = df_filtered_mission["Left_Power"].mean()
        mean_right_power = df_filtered_mission["Right_Power"].mean()
        #------------------------------------------------------#
        max_panel_voltage = df_filtered_mission["Panel_Voltage"].max()
        max_panel_power = df_filtered_mission["Panel_Power"].max()
        max_battery_voltage = df_filtered_mission["Battery_Voltage"].max()
        max_battery_power = df_filtered_mission["Battery_Power"].max()
        max_electronic_power = df_filtered_mission["Electronic_Power"].max()
        max_acc_power = df_filtered_mission["Accessories_Power"].max()
        max_left_power = df_filtered_mission["Left_Power"].max()
        max_right_power = df_filtered_mission["Right_Power"].max()
        #------------------------------------------------------#
        min_panel_voltage = df_filtered_mission["Panel_Voltage"].min()
        min_panel_power = df_filtered_mission["Panel_Power"].min()
        min_battery_voltage = df_filtered_mission["Battery_Voltage"].min()
        min_battery_power = df_filtered_mission["Battery_Power"].min()
        min_electronic_power = df_filtered_mission["Electronic_Power"].min()
        min_acc_power = df_filtered_mission["Accessories_Power"].min()
        min_left_power = df_filtered_mission["Left_Power"].min()
        min_right_power = df_filtered_mission["Right_Power"].min()

        if df_filtered_mission.empty:
          st.error("Não há dados de missão para esse robô nesse período.")
        else:
            match chart_type:
              case "Line":
                  fig_panel_voltage = px.line(df_filtered_mission, x="Time", y="Panel_Voltage", 
                                              color="Robot", title="Panel Voltage", markers=False)
                  col1.plotly_chart(fig_panel_voltage)
                  col1.write(f"**🔝 Peak: {round(max_panel_voltage,2)}V**")
                  col1.write(f"**📊 Average: {round(mean_panel_voltage,2)}V**")
                  col1.write(f"**🆘 Min: {round(min_panel_voltage,2)}V**")


                  fig_panel_power = px.line(df_filtered_mission, x="Time", y="Panel_Power",
                                          color="Robot", title="Panel Power", markers=False)
                  col2.plotly_chart(fig_panel_power)
                  col2.write(f"**🔝 Peak: {round(max_panel_power,2)}W**")
                  col2.write(f"**📊 Average: {round(mean_panel_power,2)}W**")
                  col2.write(f"**🆘 Min: {round(min_panel_power,2)}W**")

                  fig_battery_voltage = px.line(df_filtered_mission, x="Time", y="Battery_Voltage", 
                                      color="Robot", title="Battery Voltage", markers=False)
                  col3.plotly_chart(fig_battery_voltage)
                  col3.write(f"**🔝 Peak: {round(max_battery_voltage,2)}V**")
                  col3.write(f"**📊 Average: {round(mean_battery_voltage,2)}V**")
                  col3.write(f"**🆘 Min: {round(min_battery_voltage,2)}V**")

                  fig_battery_power = px.line(df_filtered_mission, x="Time", y="Battery_Power",
                                              color="Robot", title="Battery Power", markers=False)
                  col4.plotly_chart(fig_battery_power)
                  col4.write(f"**🔝 Peak: {round(max_battery_power,2)}W**")
                  col4.write(f"**📊 Average: {round(mean_battery_power,2)}W**")
                  col4.write(f"**🆘 Min: {round(min_battery_power,2)}W**")


                  fig_eletronic_power = px.line(df_filtered_mission, x="Time", y="Electronic_Power",
                                              color="Robot", title="Eletronic Power", markers=False)
                  col5.plotly_chart(fig_eletronic_power)
                  col5.write(f"**🔝 Peak: {round(max_electronic_power,2)}W**")
                  col5.write(f"**📊 Average: {round(mean_electronic_power,2)}W**")
                  col5.write(f"**🆘 Min: {round(min_electronic_power,2)}W**")


                  fig_acc_power = px.line(df_filtered_mission, x="Time", y="Accessories_Power",
                                          color="Robot", title="ACC Power", markers=False)
                  col6.plotly_chart(fig_acc_power)
                  col6.write(f"**🔝 Peak: {round(max_acc_power,2)}W**")
                  col6.write(f"**📊 Average: {round(mean_acc_power,2)}W**")
                  col6.write(f"**🆘 Min: {round(min_acc_power,2)}W**")


                  motor_left_power = px.line(df_filtered_mission, x="Time", y="Left_Power",
                                          color="Robot", title="Left Power", markers=False)
                  col7.plotly_chart(motor_left_power)
                  col7.write(f"**🔝 Peak: {round(max_left_power,2)}W**")
                  col7.write(f"**📊 Average: {round(mean_left_power,2)}W**")
                  col7.write(f"**🆘 Min: {round(min_left_power,2)}W**")

                  motor_right_power = px.line(df_filtered_mission, x="Time", y="Right_Power",
                                          color="Robot", title="Right Power", markers=False)
                  col8.plotly_chart(motor_right_power)
                  col8.write(f"**🔝 Peak: {round(max_right_power,2)}W**")
                  col8.write(f"**📊 Average: {round(mean_right_power,2)}W**")
                  col8.write(f"**🆘 Min: {round(min_right_power,2)}W**")
              case "Column":

                  fig_panel_voltage = px.bar(df_filtered_mission, x="Time", y="Panel_Voltage", 
                                              color="Robot", title="Panel Voltage")
                  col1.plotly_chart(fig_panel_voltage)
                  col1.write(f"**🔝 Peak: {round(max_panel_voltage,2)}V**")
                  col1.write(f"**📊 Average: {round(mean_panel_voltage,2)}V**")
                  col1.write(f"**🆘 Min: {round(min_panel_voltage,2)}V**")  

                  fig_panel_power = px.bar(df_filtered_mission, x="Time", y="Panel_Power",
                                          color="Robot", title="Panel Power")
                  col2.plotly_chart(fig_panel_power)
                  col2.write(f"**🔝 Peak: {round(max_panel_power,2)}W**")
                  col2.write(f"**📊 Average: {round(mean_panel_power,2)}W**")
                  col2.write(f"**🆘 Min: {round(min_panel_power,2)}W**")

                  fig_battery_voltage = px.bar(df_filtered_mission, x="Time", y="Battery_Voltage", 
                                      color="Robot", title="Battery Voltage")
                  col3.plotly_chart(fig_battery_voltage)
                  col3.write(f"**🔝 Peak: {round(max_battery_voltage,2)}V**")
                  col3.write(f"**📊 Average: {round(mean_battery_voltage,2)}V**")
                  col3.write(f"**🆘 Min: {round(min_battery_voltage,2)}V**")

                  fig_battery_power = px.bar(df_filtered_mission, x="Time", y="Battery_Power",
                                              color="Robot", title="Battery Power")
                  col4.plotly_chart(fig_battery_power)
                  col4.write(f"**🔝 Peak: {round(max_battery_power,2)}W**")
                  col4.write(f"**📊 Average: {round(mean_battery_power,2)}W**")
                  col4.write(f"**🆘 Min: {round(min_battery_power,2)}W**")

                  fig_eletronic_power = px.bar(df_filtered_mission, x="Time", y="Electronic_Power",
                                              color="Robot", title="Eletronic Power")
                  col5.plotly_chart(fig_eletronic_power)
                  col5.write(f"**🔝 Peak: {round(max_electronic_power,2)}W**")
                  col5.write(f"**📊 Average: {round(mean_electronic_power,2)}W**")
                  col5.write(f"**🆘 Min: {round(min_electronic_power,2)}W**")


                  fig_acc_power = px.bar(df_filtered_mission, x="Time", y="Accessories_Power",
                                          color="Robot", title="ACC Power")
                  col6.plotly_chart(fig_acc_power)
                  col6.write(f"**🔝 Peak: {round(max_acc_power,2)}W**")
                  col6.write(f"**📊 Average: {round(mean_acc_power,2)}W**")
                  col6.write(f"**🆘 Min: {round(min_acc_power,2)}W**")

                  motor_left_power = px.bar(df_filtered_mission, x="Time", y="Left_Power",
                                          color="Robot", title="Left Power")
                  col7.plotly_chart(motor_left_power)
                  col7.write(f"**🔝 Peak: {round(max_left_power,2)}W**")
                  col7.write(f"**📊 Average: {round(mean_left_power,2)}W**")
                  col7.write(f"**🆘 Min: {round(min_left_power,2)}W**")

                  motor_right_power = px.bar(df_filtered_mission, x="Time", y="Right_Power",
                                          color="Robot", title="Right Power")
                  col8.plotly_chart(motor_right_power)
                  col8.write(f"**🔝 Peak: {round(max_right_power,2)}W**")
                  col8.write(f"**📊 Average: {round(mean_right_power,2)}W**")
                  col8.write(f"**🆘 Min: {round(min_right_power,2)}W**")
              case "Box":
                  fig_panel_voltage = px.box(df_filtered_mission, y="Panel_Voltage", 
                                              color="Robot", title="Panel Voltage")
                  col1.plotly_chart(fig_panel_voltage)
                  col1.write(f"**🔝 Peak: {round(max_panel_voltage,2)}V**")
                  col1.write(f"**📊 Average: {round(mean_panel_voltage,2)}V**")
                  col1.write(f"**🆘 Min: {round(min_panel_voltage,2)}V**")

                  fig_panel_power = px.box(df_filtered_mission,  y="Panel_Power",
                                          color="Robot", title="Panel Power")
                  col2.plotly_chart(fig_panel_power)
                  col2.write(f"**🔝 Peak: {round(max_panel_power,2)}W**")
                  col2.write(f"**📊 Average: {round(mean_panel_power,2)}W**")
                  col2.write(f"**🆘 Min: {round(min_panel_power,2)}W**")

                  fig_battery_voltage = px.box(df_filtered_mission,  y="Battery_Voltage", 
                                      color="Robot", title="Battery Voltage")
                  col3.plotly_chart(fig_battery_voltage)
                  col3.write(f"**🔝 Peak: {round(max_battery_voltage,2)}V**")
                  col3.write(f"**📊 Average: {round(mean_battery_voltage,2)}V**")
                  col3.write(f"**🆘 Min: {round(min_battery_voltage,2)}V**")

                  fig_battery_power = px.box(df_filtered_mission,  y="Battery_Power",
                                              color="Robot", title="Battery Power")
                  col4.plotly_chart(fig_battery_power)
                  col4.write(f"**🔝 Peak: {round(max_battery_power,2)}W**")
                  col4.write(f"**📊 Average: {round(mean_battery_power,2)}W**")
                  col4.write(f"**🆘 Min: {round(min_battery_power,2)}W**")

                  fig_eletronic_power = px.box(df_filtered_mission,  y="Electronic_Power",
                                              color="Robot", title="Eletronic Power")
                  col5.plotly_chart(fig_eletronic_power)
                  col5.write(f"**🔝 Peak: {round(max_electronic_power,2)}W**")
                  col5.write(f"**📊 Average: {round(mean_electronic_power,2)}W**")
                  col5.write(f"**🆘 Min: {round(min_electronic_power,2)}W**")

                  fig_acc_power = px.box(df_filtered_mission,  y="Accessories_Power",
                                          color="Robot", title="ACC Power")
                  col6.plotly_chart(fig_acc_power)
                  col6.write(f"**🔝 Peak: {round(max_acc_power,2)}W**")
                  col6.write(f"**📊 Average: {round(mean_acc_power,2)}W**")
                  col6.write(f"**🆘 Min: {round(min_acc_power,2)}W**")

                  motor_left_power = px.box(df_filtered_mission,  y="Left_Power",
                                          color="Robot", title="Left Power")
                  col7.plotly_chart(motor_left_power)
                  col7.write(f"**🔝 Peak: {round(max_left_power,2)}W**")
                  col7.write(f"**📊 Average: {round(mean_left_power,2)}W**")
                  col7.write(f"**🆘 Min: {round(min_left_power,2)}W**")

                  motor_right_power = px.box(df_filtered_mission,  y="Right_Power",
                                          color="Robot", title="Right Power")
                  col8.plotly_chart(motor_right_power)
                  col8.write(f"**🔝 Peak: {round(max_right_power,2)}W**")
                  col8.write(f"**📊 Average: {round(mean_right_power,2)}W**")
                  col8.write(f"**🆘 Min: {round(min_right_power,2)}W**")
              case "Histogram":
                  fig_panel_voltage = px.histogram(df_filtered_mission, x="Panel_Voltage", 
                                              color="Robot", title="Panel Voltage")
                  col1.plotly_chart(fig_panel_voltage)
                  col1.write(f"**🔝 Peak: {round(max_panel_voltage,2)}V**")
                  col1.write(f"**📊 Average: {round(mean_panel_voltage,2)}V**")
                  col1.write(f"**🆘 Min: {round(min_panel_voltage,2)}V**")


                  fig_panel_power = px.histogram(df_filtered_mission,  x="Panel_Power",
                                          color="Robot", title="Panel Power")
                  col2.plotly_chart(fig_panel_power)
                  col2.write(f"**🔝 Peak: {round(max_panel_power,2)}W**")
                  col2.write(f"**📊 Average: {round(mean_panel_power,2)}W**")
                  col2.write(f"**🆘 Min: {round(min_panel_power,2)}W**")

                  fig_battery_voltage = px.histogram(df_filtered_mission,  x="Battery_Voltage", 
                                      color="Robot", title="Battery Voltage")
                  col3.plotly_chart(fig_battery_voltage)
                  col3.write(f"**🔝 Peak: {round(max_battery_voltage,2)}V**")
                  col3.write(f"**📊 Average: {round(mean_battery_voltage,2)}V**")
                  col3.write(f"**🆘 Min: {round(min_battery_voltage,2)}V**")

                  fig_battery_power = px.histogram(df_filtered_mission,  x="Battery_Power",
                                              color="Robot", title="Battery Power")
                  col4.plotly_chart(fig_battery_power)
                  col4.write(f"**🔝 Peak: {round(max_battery_power,2)}W**")
                  col4.write(f"**📊 Average: {round(mean_battery_power,2)}W**")
                  col4.write(f"**🆘 Min: {round(min_battery_power,2)}W**")


                  fig_eletronic_power = px.histogram(df_filtered_mission,  x="Electronic_Power",
                                              color="Robot", title="Eletronic Power")
                  col5.plotly_chart(fig_eletronic_power)
                  col5.write(f"**🔝 Peak: {round(max_electronic_power,2)}W**")
                  col5.write(f"**📊 Average: {round(mean_electronic_power,2)}W**")
                  col5.write(f"**🆘 Min: {round(min_electronic_power,2)}W**")


                  fig_acc_power = px.histogram(df_filtered_mission,  x="Accessories_Power",
                                          color="Robot", title="ACC Power")
                  col6.plotly_chart(fig_acc_power)
                  col6.write(f"**🔝 Peak: {round(max_acc_power,2)}W**")
                  col6.write(f"**📊 Average: {round(mean_acc_power,2)}W**")
                  col6.write(f"**🆘 Min: {round(min_acc_power,2)}W**")


                  motor_left_power = px.histogram(df_filtered_mission,  x="Left_Power",
                                          color="Robot", title="Left Power")
                  col7.plotly_chart(motor_left_power)
                  col7.write(f"**🔝 Peak: {round(max_left_power,2)}W**")
                  col7.write(f"**📊 Average: {round(mean_left_power,2)}W**")
                  col7.write(f"**🆘 Min: {round(min_left_power,2)}W**")

                  motor_right_power = px.histogram(df_filtered_mission,  x="Right_Power",
                                          color="Robot", title="Right Power")
                  col8.plotly_chart(motor_right_power)
                  col8.write(f"**🔝 Peak: {round(max_right_power,2)}W**")
                  col8.write(f"**📊 Average: {round(mean_right_power,2)}W**")
                  col8.write(f"**🆘 Min: {round(min_right_power,2)}W**")

              case "Average Values":  
                  col1.write(f"**Average Panel Voltage: {round(mean_panel_voltage,2)}V**")
                  col2.write(f"**Average Panel Power: {round(mean_panel_power,2)}W**")
                  col1.write(f"**Average Battery Voltage: {round(mean_battery_voltage,2)}V**")
                  col2.write(f"**Average Battery Power: {round(mean_panel_power,2)}W**")
                  col1.write(f"**Average Eletronic Power: {round(mean_electronic_power,2)}W**")
                  col2.write(f"**Average ACC Power: {round(mean_acc_power,2)}W**")
                  col1.write(f"**Average Left Motor Power: {round(mean_left_power,2)}W**")
                  col2.write(f"**Average Right Motor Power: {round(mean_right_power,2)}W**")
                  robot_consumption = round(mean_battery_power/mean_battery_voltage)
                  col1.write(f"**Mean Robots Consumption: {robot_consumption}A**")
                  robot_generate = round(mean_panel_power/mean_panel_voltage)
                  col2.write(f"**Mean Robots Generation: {robot_generate}A**")
                
                  fig_panel_voltage = px.line(df_filtered_mission, x="Time", y="Panel_Voltage", color="Robot", title="Panel Voltage", markers=False)
                  fig_panel_voltage.add_shape(
                      go.layout.Shape(
                          type="line",
                          x0=df_filtered_mission['Time'].min(),
                          x1=df_filtered_mission['Time'].max(),
                          y0=mean_panel_voltage,
                          y1=mean_panel_voltage,
                          line=dict(color="red", width=2)
                      )
                  )
                  col1.plotly_chart(fig_panel_voltage)

                  fig_panel_power = px.line(df_filtered_mission, x="Time", y="Panel_Power", color="Robot", title="Average Panel Power", markers=False)
                  fig_panel_power.add_shape(
                      go.layout.Shape(
                          type="line",
                          x0=df_filtered_mission['Time'].min(),
                          x1=df_filtered_mission['Time'].max(),
                          y0=mean_panel_power,
                          y1=mean_panel_power,
                          line=dict(color="red", width=2)
                      )
                  )
                  col2.plotly_chart(fig_panel_power)

                  fig_battery_voltage = px.line(df_filtered_mission, x="Time", y="Battery_Voltage", color="Robot", title="Average Battery Voltage", markers=False)
                  fig_battery_voltage.add_shape(
                      go.layout.Shape(
                          type="line",
                          x0=df_filtered_mission['Time'].min(),
                          x1=df_filtered_mission['Time'].max(),
                          y0=mean_battery_voltage,
                          y1=mean_battery_voltage,
                          line=dict(color="red", width=2)
                      )
                  )
                  col3.plotly_chart(fig_battery_voltage)

                  fig_battery_power = px.line(df_filtered_mission, x="Time", y="Battery_Power", color="Robot", title="Average Battery Power", markers=False)
                  fig_battery_power.add_shape(
                      go.layout.Shape(
                          type="line",
                          x0=df_filtered_mission['Time'].min(),
                          x1=df_filtered_mission['Time'].max(),
                          y0=mean_battery_power,
                          y1=mean_battery_power,
                          line=dict(color="red", width=2)
                      )
                  )
                  col4.plotly_chart(fig_battery_power)

                  fig_eletronic_power = px.line(df_filtered_mission, x="Time", y="Electronic_Power", color="Robot", title="Average Electronic Power", markers=False)
                  fig_eletronic_power.add_shape(
                      go.layout.Shape(
                          type="line",
                          x0=df_filtered_mission['Time'].min(),
                          x1=df_filtered_mission['Time'].max(),
                          y0=mean_electronic_power,
                          y1=mean_electronic_power,
                          line=dict(color="red", width=2)
                      )
                  )
                  col5.plotly_chart(fig_eletronic_power)

                  fig_acc_power = px.line(df_filtered_mission, x="Time", y="Accessories_Power", color="Robot", title="Average ACC Power", markers=False)
                  fig_acc_power.add_shape(
                      go.layout.Shape(
                          type="line",
                          x0=df_filtered_mission['Time'].min(),
                          x1=df_filtered_mission['Time'].max(),
                          y0=mean_acc_power,
                          y1=mean_acc_power,
                          line=dict(color="red", width=2)
                      )
                  )
                  col6.plotly_chart(fig_acc_power)

                  fig_left_power = px.line(df_filtered_mission, x="Time", y="Left_Power", color="Robot", title="Average Motor Left Power", markers=False)
                  fig_left_power.add_shape(
                      go.layout.Shape(
                          type="line",
                          x0=df_filtered_mission['Time'].min(),
                          x1=df_filtered_mission['Time'].max(),
                          y0=mean_left_power,
                          y1=mean_left_power,
                          line=dict(color="red", width=2)
                      )
                  )
                  col7.plotly_chart(fig_left_power)

                  fig_right_power = px.line(df_filtered_mission, x="Time", y="Right_Power", color="Robot", title="Average Motor Right Power", markers=False)
                  fig_right_power.add_shape(
                      go.layout.Shape(
                          type="line",
                          x0=df_filtered_mission['Time'].min(),
                          x1=df_filtered_mission['Time'].max(),
                          y0=mean_right_power,
                          y1=mean_right_power,
                          line=dict(color="red", width=2)
                      )
                  )
                  col8.plotly_chart(fig_right_power)

      elif mean_period == ":rainbow[Mission DataFrame] :floppy_disk:":
        
        df_filtered_mission = df[
        (df["Date"] == date) & 
        (df["Robot"] == robot) & 
        (df["GPS_Speed"] > 0.3) & 
        (df["Last_Update"] == 0) & 
        (df["Remote_Control"] != 'RADIO') & 
        (df["GPS_Status"] == 44)]
        
        if df_filtered_mission.empty:
          st.error("Não há dados para este robô")
        else:
          df_filtered_mission

      elif mean_period == ":rainbow[Daily DataFrame] :floppy_disk:":
        df_filtered_date




