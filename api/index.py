from flask import Flask, request, jsonify, redirect
from flask_mail import Mail, Message
from urllib.parse import quote, unquote
import pandas as pd
import os
from datetime import datetime


app = Flask(__name__)

# Configuración del servidor de correo
app.config.update(
    MAIL_SERVER='sandbox.smtp.mailtrap.io',
    MAIL_PORT='2525',
    MAIL_USERNAME='a95a9e3917b07b',
    MAIL_PASSWORD='fc21159a96480c',
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False
)

mail = Mail(app)

EXCEL_FILE = 'auditoria_clicks.xlsx'

# Inicializar archivo Excel si no existe
def init_excel():
    if not os.path.exists(EXCEL_FILE):
        df = pd.DataFrame(columns=['email', 'clicked', 'clicked_at', 'ip'])
        df.to_excel(EXCEL_FILE, index=False)

init_excel()

@app.route('/send-audit-emails', methods=['POST'])
def send_audit_emails():
    try:
        from_email = request.json.get('from_email', None)
        subject = request.json.get('subject', None)
        emails = request.json.get('emails', [])
        if not isinstance(emails, list) or not emails:
            return jsonify({'status': 'error', 'message': 'Lista inválida'}), 400

        for email in emails:
            date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            link = f"http://127.0.0.1:5000/track-click/{quote(email)}"

            html = generate_pdf_html(email, date, link)
            
            msg = Message(
               
                subject=subject,
                          sender=from_email,
                          recipients=[email],
                          html=html)
            mail.send(msg)

        return jsonify({'status': 'success', 'message': 'Correos enviados correctamente'}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500





@app.route('/track-click/<email_encoded>')
def track_click(email_encoded):
    try:
        email = unquote(email_encoded)
        ip = request.remote_addr
        timestamp = datetime.utcnow().isoformat()

        # Cargar Excel existente
        df = pd.read_excel(EXCEL_FILE)

        # Verificar si el correo ya existe
        updated = False
        for idx, row in df.iterrows():
            if row['email'] == email:
                df.at[idx, 'clicked'] = 'yes'
                df.at[idx, 'clicked_at'] = timestamp
                df.at[idx, 'ip'] = ip
                updated = True
                break

        # Si no existe, lo agrega
        if not updated:
            df = pd.concat([df, pd.DataFrame([{
                'email': email,
                'clicked': 'yes',
                'clicked_at': timestamp,
                'ip': ip
            }])], ignore_index=True)

        df.to_excel(EXCEL_FILE, index=False)

        # Redirige al PDF o página de destino
        return redirect(f"https://www.ecuadordirectroses.com/api/audit/pdf?email={quote(email)}")

    except Exception as e:
        return f"Error: {e}", 500


def generate_pdf_html(email, date ,link):
    # Generar el HTML para el PDF

    html = f"""
                <div bgcolor="#ffffff" marginwidth="0" marginheight="0">
<table id="m_-7786020817345657024Tabla_01" height="794" cellspacing="0" cellpadding="0" width="850" border="0">
  <tbody>
  <tr>
    <td><img alt="" src="https://ci3.googleusercontent.com/meips/ADKq_NY_U4SzUJ8vfITKohHLCoua6lvAjDEDyOORSdlHmioTVDA6yOm9FPfBarrP1R7AL_Ge4VfEm9s2GjCsUM4NUfUlttAk9Kiw5wL0QXvZDKSVPVlaMtNT0Ldl9xP6YMNxhl1MaClm=s0-d-e1-ft#https://content.prd.net.ec/beprod/produbanco-enlinea-notificacion-170221_02.jpg" width="850" height="218" class="CToWUd a6T" data-bit="iit" tabindex="0"><div class="a6S" dir="ltr" style="opacity: 0.01; left: 810px; top: 181px;"><span data-is-tooltip-wrapper="true" class="a5q" jsaction="JIbuQc:.CLIENT"><button class="VYBDae-JX-I VYBDae-JX-I-ql-ay5-ays CgzRE" jscontroller="PIVayb" jsaction="click:h5M12e; clickmod:h5M12e;pointerdown:FEiYhc;pointerup:mF5Elf;pointerenter:EX0mI;pointerleave:vpvbp;pointercancel:xyn4sd;contextmenu:xexox;focus:h06R8; blur:zjh6rb;mlnRJb:fLiPzd;" data-idom-class="CgzRE" data-use-native-focus-logic="true" jsname="hRZeKc" aria-label="Descargar el archivo adjunto " data-tooltip-enabled="true" data-tooltip-id="tt-c38" data-tooltip-classes="AZPksf" id="" jslog="91252; u014N:cOuCgd,Kr2w4b,xr6bB; 4:WyIjbXNnLWY6MTgzNzgzODY4Mzc0MDk2NDcxMSJd; 43:WyJpbWFnZS9qcGVnIl0."><span class="OiePBf-zPjgPe VYBDae-JX-UHGRz"></span><span class="bHC-Q" jscontroller="LBaJxb" jsname="m9ZlFb" soy-skip="" ssk="6:RWVI5c"></span><span class="VYBDae-JX-ank-Rtc0Jf" jsname="S5tZuc" aria-hidden="true"><span class="notranslate bzc-ank" aria-hidden="true"><svg viewBox="0 -960 960 960" height="20" width="20" focusable="false" class=" aoH"><path d="M480-336L288-528l51-51L444-474V-816h72v342L621-579l51,51L480-336ZM263.72-192Q234-192 213-213.15T192-264v-72h72v72H696v-72h72v72q0,29.7-21.16,50.85T695.96-192H263.72Z"></path></svg></span></span><div class="VYBDae-JX-ano"></div></button><div class="ne2Ple-oshW8e-J9" id="tt-c38" role="tooltip" aria-hidden="true">Descargar</div></span></div></td></tr>
  <tr>
    <td>
      <table cellspacing="40" width="100%">
        <tbody>
        <tr>
          <td>
            <p><font face="Nunito Sans Normal">Estimado/a</font></p>
            <p><font face="Nunito Sans Normal">{email}</font></p>
            <p><font face="Nunito Sans Normal">Fecha y Hora: {date}</font></p>
            <p><font face="Nunito Sans Normal">Transacción: <strong>Consumo 
            Tarjeta de Débito Produbanco</strong></font></p>
            <p><font face="Nunito Sans Normal">Te informamos que se acaba de 
            registrar un consumo con tu Tarjeta de Débito Produbanco.</font></p>
            <p><strong><font face="Nunito Sans Normal">Detalle</font></strong></p>
            <p><font face="Nunito Sans Normal"><strong>Valor:</strong> 
            USD 10.50<br><strong>Establecimiento:</strong> 
            CLARO PORTAL CAUTIVO K   Guayaquil    EC<br><strong>Cuenta Débito:</strong> 
            CNA XXXXXX22281</font></p>
            <p><font face="Nunito Sans Normal"></font></p>
            <p><font face="Nunito Sans Normal">Atentamente 
          Produbanco</font></p>

          <p><font face="Nunito Sans Normal">
            <a href="{link}" target="_blank">Ver en el portal</a>
          </font></p>
          
          </td></tr></tbody></table>
      <p>&nbsp;</p></td></tr>
  <tr>
    <td>
      <table cellspacing="0" width="100%">
        <tbody>
        <tr>
          <td colspan="6"><img alt="" src="https://ci3.googleusercontent.com/meips/ADKq_NZ4N-VpH05rBbU5HuXaJrqhUU-VY-15X6ukkJ8lMP_OT86wBR1_ecPRkfvPepgn0elDUfefk2bTD2eVrf8dDP9SSeTR88wfKkzmpdeBXlOFyfBMi8wUdqOXOpXv9AOety3Vfw3W=s0-d-e1-ft#https://content.prd.net.ec/beprod/produbanco-enlinea-notificacion-190221_01.jpg" width="850" height="41" class="CToWUd" data-bit="iit"></td></tr>
        <tr>
          <td colspan="6"><a href="{link}" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://www.produbanco.com.ec/&amp;source=gmail&amp;ust=1752856138322000&amp;usg=AOvVaw0B4S9o8hQc34groHXc5w4h"><img border="0" alt="" src="https://ci3.googleusercontent.com/meips/ADKq_NaecS5ckLkajYsDUWZio7MNYN3uHM8fjtNLAiDotrza2DmyMM0BPnHfCAfHNHZ2qa9RP2eIjpaowKMSPhhPDyBUmDLRVD_Byzk4P3A4h4zZ3U0QpYKGG0u0R9_yFJ2H2SQi2CM3=s0-d-e1-ft#https://content.prd.net.ec/beprod/produbanco-enlinea-notificacion-190221_02.jpg" width="850" height="26" class="CToWUd" data-bit="iit"></a></td></tr>
        <tr>
          <td><img alt="" src="https://ci3.googleusercontent.com/meips/ADKq_NaHHLdvRGF0NhC2t4U4gbuUHr55LxiQr_sTUgKudsJEhZtMhTSxXC6Hx_c6gTBfFO6Ce-MLp9060ufGsi1aaxxZRJ0Si7OVCW9R2bUGLtkOYqpq0h2MrCIUYHJH4429SbmlIrbv=s0-d-e1-ft#https://content.prd.net.ec/beprod/produbanco-enlinea-notificacion-190221_03.jpg" width="37" height="37" class="CToWUd" data-bit="iit"></td>
          <td><a href="{link}" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://www.facebook.com/Produbanco&amp;source=gmail&amp;ust=1752856138322000&amp;usg=AOvVaw0iT1qj-2bcB2J9T7oMUJiF"><img border="0" alt="" src="https://ci3.googleusercontent.com/meips/ADKq_NYbHdQUH_9On9b-1f6HqhLrS6iLZbJ1wvLJz389TtcLcZWOql2YTHN1Ozzf7gW5UEX2PoQ-8YT_L4gNpRoyIe_1HKo7CtgN88evhwIkfYqXJ8ve0raE6rv2W_XUqURC7XflJLAH=s0-d-e1-ft#https://content.prd.net.ec/beprod/produbanco-enlinea-notificacion-190221_04.jpg" width="38" height="37" class="CToWUd" data-bit="iit"></a></td>
          <td><a href="{link}" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://twitter.com/produbancoec&amp;source=gmail&amp;ust=1752856138322000&amp;usg=AOvVaw3ycUxkimn3xSTWdCz66rPC"><img border="0" alt="" src="https://ci3.googleusercontent.com/meips/ADKq_NYJVrWfdid6fcaJ2KztsygMdL3L_eTWm5ItVAtmpG1Y1CYCfB4QHEosxAbxZPbiBaij6PAaBWgb03yzDqBn7PnyhURgKre-ZH7M2v1zO7d5cS9dNaUpQj3ymaCn8qs2iN2sRORP=s0-d-e1-ft#https://content.prd.net.ec/beprod/produbanco-enlinea-notificacion-190221_05.jpg" width="37" height="37" class="CToWUd" data-bit="iit"></a></td>
          <td><a href="{link}" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://www.instagram.com/produbancoec/&amp;source=gmail&amp;ust=1752856138322000&amp;usg=AOvVaw2l3XCB2xYybdZfza7aj5n2"><img border="0" alt="" src="https://ci3.googleusercontent.com/meips/ADKq_NYT58i3GHz619PC0Vg7I3gyyHW2tfExLt81HVEJcfXueD9JgaTMCkMpSBzF8doild-jPZGbD3t7CnbFTSgO2u0UBNnB7I6eGPpPx5y2lHtVtUgycUbqa0bO4gbTTYuFtMuCWRR6=s0-d-e1-ft#https://content.prd.net.ec/beprod/produbanco-enlinea-notificacion-190221_06.jpg" width="34" height="37" class="CToWUd" data-bit="iit"></a></td>
          <td><a href="{link}" target="_blank" data-saferedirecturl="https://www.google.com/url?q=http://wa.me/593024009000&amp;source=gmail&amp;ust=1752856138322000&amp;usg=AOvVaw26xQX26KJNT6UqvgfqI5uX"><img border="0" alt="" src="https://ci3.googleusercontent.com/meips/ADKq_NbJkykIU7iTT4YOicOpYVDg1dk9-2NzS0t6WTANHDlgtjyTN5kIs644UxMnjl9epzucRyHcKyWGqpw3MZAPsmdFipCriDb6L1N41hlPk98_KjdgAOUX2Luaas_Dqs3b5aHrQDzi=s0-d-e1-ft#https://content.prd.net.ec/beprod/produbanco-enlinea-notificacion-190221_07.jpg" width="35" height="37" class="CToWUd" data-bit="iit"></a></td>
          <td><img alt="" src="https://ci3.googleusercontent.com/meips/ADKq_NYOZNW9uCazTpAlw1iX66LBYKpjrma_lJcDL1cRrQBobH1GDyX_3s-Fes-TYTUGiNcI2J8jsE_nqLEiLFlZ9edWKh5LvoBQUht63KjHLWNapcIDT7nuUqSg-ibH4Bhzls37Yzto=s0-d-e1-ft#https://content.prd.net.ec/beprod/produbanco-enlinea-notificacion-190221_08.jpg" width="669" height="37" class="CToWUd" data-bit="iit"></td></tr>
        <tr>
        


<div>
<table width="720" cellspacing="0" cellpadding="0" border="0" bgcolor="#ffffff">
  <tbody><tr>
    <td><br></td>
    <td>&nbsp;</td>
  </tr>
  <tr>
    <td><table width="100%" cellspacing="0" cellpadding="0" border="0" align="center">
      <tbody><tr>
        <td colspan="2"><div align="justify">Si tienes alguna consulta con respecto a esta información no dudes en comunicarte con nosotros, caso contrario no es necesario responder a este correo electrónico.</div><div align="justify"><div align="justify"><div align="justify">La información y adjuntos contenidos en este mensaje son confidenciales y reservados; por tanto no pueden ser usados, reproducidos o divulgados por otras personas distintas a su(s) destinatario(s). Si no eres el destinatario de este email, te solicitamos comedidamente eliminarlo. Cualquier opinión expresada en este mensaje, corresponde a su autor y no necesariamente al Banco.</div><div align="justify">Recuerda que Produbanco nunca te requerirá por ningún medio, tu usuario o clave de acceso a sus sitios web o aplicaciones móviles.</div><div align="justify">Te recomendamos no imprimir este correo electrónico a menos que sea estrictamente necesario.</div><div><br></div></div><div><br></div></div></td>       
      </tr>	
    </tbody></table></td>
  </tr>
</tbody></table><div class="yj6qo"></div><div class="adL">
</div></div><div class="adL">

</div></div>
            """

    return html


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
