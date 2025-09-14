import smtplib
import datetime
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(body):
    """Send email reminder using Streamlit secrets."""
    try:
        # Get credentials from Streamlit secrets
        password = st.secrets["email"]["password"]
        sender_email = st.secrets["email"]["sender_email"]
        recipient_email = st.secrets["email"]["recipient_email"]
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "🧠 SPACED REPETITION REMINDER"
        
        # Add timestamp
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_body = f"⏰ Time: {current_time}\n\n📝 Task: {body}\n\n💡 Complete this task and mark your progress!"
        
        msg.attach(MIMEText(full_body, 'plain'))
        
        # Send email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
            
        print(f"✅ Email sent successfully: {body}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        st.error(f"Email sending failed: {e}")
        return False