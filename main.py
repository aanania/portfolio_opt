from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from io import BytesIO

app = FastAPI()

@app.post("/optimize-portfolio")
async def optimize_portfolio(
    file: UploadFile = File(...),
    risk_level: float = Form(...),
    max_weight: float = Form(...)
):
    try:
        # Leer el archivo CSV
        contents = await file.read()
        df = pd.read_csv(BytesIO(contents), index_col=0, parse_date=True, date_format="%Y-%m-%d")
        df = df.dropna(how="all")
        df = df.fillna(0)  # llena retornos vacios con 0s

        # Validación de datos
        if df.isnull().values.any():
            raise ValueError("El archivo contiene valores nulos.")
        if df.shape[1] < 2:
            raise ValueError("Se requieren al menos 2 activos para optimizar un portafolio.")

        tickers = df.columns.tolist()
        returns = df.to_numpy()
        mean_returns = np.mean(returns, axis=0)
        cov_matrix = np.cov(returns.T)

        num_assets = len(tickers)

        # Restricciones
        constraints = (
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},  # suma de pesos = 1
            {'type': 'ineq', 'fun': lambda w: risk_level - np.sqrt(np.dot(w.T, np.dot(cov_matrix, w)))}  # riesgo máximo
        )
        bounds = tuple((0, max_weight) for _ in range(num_assets))
        initial_guess = num_assets * [1. / num_assets]

        # Función objetivo: minimizar varianza negativa para maximizar retorno ajustado a riesgo
        def neg_sharpe_ratio(w):
            port_return = np.dot(w, mean_returns)
            port_risk = np.sqrt(np.dot(w.T, np.dot(cov_matrix, w)))
            if port_risk == 0:
                return np.inf
            return -port_return / port_risk

        result = minimize(
            neg_sharpe_ratio,
            initial_guess,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )

        if not result.success:
            raise ValueError("Optimización fallida: " + result.message)

        weights = result.x
        optimized_portfolio = {
            ticker: round(weight, 4) for ticker, weight in zip(tickers, weights)
        }

        return JSONResponse(content={
            "optimized_weights": optimized_portfolio,
            "expected_return": round(float(np.dot(weights, mean_returns)), 4),
            "expected_risk": round(float(np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))), 4)
        })

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
