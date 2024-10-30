from fastapi import FastAPI, Request, Response, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

from src.services.serializers import validate_email
from src.services.main_service import get_client_by_email, create_client, authorize_client, evaluate_client


SIGNUP_FIELDS = ['gender', 'first_name', 'last_name', 'avatar']
AVAILABLE_GENDER = ['male', 'female']

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/clients/create")


@app.post("/api/clients/create", status_code=201)
async def create_new_user(request: Request, response: Response):
    try:
        form = await request.form()
        if 'password' not in form or 'email' not in form or not validate_email(form['email']):
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": "A passport and correct email must be sent."}

        client_with_email = await get_client_by_email(form['email'])
        if not client_with_email:
            if any([bool(field not in form.keys()) for field in SIGNUP_FIELDS]):
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"detail": "Incorrect fields for user creating. "
                                  "Send fields: email, password, gender, first_name, last_name, avatar"}
            if form['gender'] not in AVAILABLE_GENDER:
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {"detail": "Incorrect gender. Available: male or female."}
            token = await create_client(form)
        else:
            token = await authorize_client(client_with_email.id, client_with_email.password, form["password"])

        if not token:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": "Wrong input client data."}
        return {"token": token}
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": "An unexpected error occurred. Contact your administrator."}


@app.post("/api/clients/{client_id}/match")
async def match_client(token: Annotated[str, Depends(oauth2_scheme)], client_id, response: Response):
    try:
        is_success, result = await evaluate_client(token, client_id)
        if not is_success:
            response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": "An unexpected error occurred. Contact your administrator."}
