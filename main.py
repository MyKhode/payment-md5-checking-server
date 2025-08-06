from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI()

# Model to handle incoming request from PHP
class CheckPaymentRequest(BaseModel):
    tran_id: str

# Function to call Bakong API using the md5 value from transaction
def check_bakong_payment(md5: str, access_token: str) -> Dict[str, Any]:
    api_url = "https://api-bakong.nbc.gov.kh/v1/check_transaction_by_md5"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    response = requests.post(api_url, json={"md5": md5}, headers=headers)
    if response.status_code == 403:
        raise HTTPException(status_code=403, detail="CloudFront blocked the request")
    
    response_data = response.json()
    return response_data

@app.post("/check-payment/")
async def check_payment(request: CheckPaymentRequest):
    # Here you will get `tran_id` and fetch its `md5` from your DB or elsewhere
    tran_id = request.tran_id
    
    # Here, you'll need the logic to retrieve `md5` and `access_token` from your DB based on `tran_id`.
    # Placeholder values for md5 and access_token
    md5 = "sample_md5_for_" + tran_id  # Replace this with your actual logic to fetch md5
    access_token = "your_bakong_access_token"  # Replace with your actual access token

    try:
        result = check_bakong_payment(md5, access_token)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking payment: {str(e)}")
