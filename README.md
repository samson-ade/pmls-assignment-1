# M10 PMLS - ASSIGNMENT 1: Model Deployment Using FastAPI

## Business Context
A skin clinic conducted a marketing campaign targeting 10,000 customers. The objective is to analyse which customer segments are more likely to respond to the campaign based on demographics and purchase behavior. Insights from this analysis will help improve future targeting strategies and increase campaign effectiveness.

---

## Results Summary

### 1. Gender vs Campaign Response
| segment | total_customers | responders | response_rate_pct |
|:---|:---:|:---:|:---:|
| Female | 6007 | 2629 | 43.77% |
| Male | 3993 | 1361 | 34.08% |

### 2. Age Group vs Campaign Response
| segment | total_customers | responders | response_rate_pct |
|:---|:---:|:---:|:---:|
| 30-50 | 4992 | 2349 | 47.06% |
| >50 | 2509 | 818 | 32.60% |
| <30 | 2499 | 823 | 32.93% |

### 3. Purchase in Last Quarter vs Campaign Response
| segment | total_customers | responders | response_rate_pct |
|:---|:---:|:---:|:---:|
| Yes | 6514 | 3234 | 49.65% |
| No | 3486 | 756 | 21.69% |

### 4. Product Usage vs Campaign Response
| segment | total_customers | responders | response_rate_pct |
|:---|:---:|:---:|:---:|
| >8 | 4206 | 2187 | 52.00% |
| 5-8 | 3703 | 1425 | 38.48% |
| 1-4 | 2091 | 378 | 18.08% |

---

## How to Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open your browser and navigate to:
- `http://127.0.0.1:8000/` (Home)
- `http://127.0.0.1:8000/campaign-analysis` (Tabular response)
- `http://127.0.0.1:8000/docs` (FastAPI Swagger UI)

---

## Deploy to Render

1. Create a new GitHub repository and push the files in this folder.
2. Sign in to [Render](https://dashboard.render.com/) and click **New +** -> **Web Service**.
3. Connect your repository.
4. Set the following build and start commands:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Click **Create Web Service**.
6. Once deployed, access your endpoint at:
   `https://<your-render-service-name>.onrender.com/campaign-analysis`
