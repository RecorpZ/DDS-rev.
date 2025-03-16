from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import csv
import json
import os
from datetime import datetime

app = FastAPI()

REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

class ReportRequest(BaseModel):
    video_filename: str
    damage_count: int
    timestamp: str

@app.post("/generate-report")
async def generate_report(report_data: ReportRequest):

    report_json = {
        "video_filename": report_data.video_filename,
        "damage_count": report_data.damage_count,
        "timestamp": report_data.timestamp,
    }

    json_filename = f"report_{report_data.video_filename}_{report_data.timestamp}.json"
    json_path = os.path.join(REPORTS_DIR, json_filename)
    with open(json_path, "w") as json_file:
        json.dump(report_json, json_file, indent=4)

    csv_filename = f"report_{report_data.video_filename}_{report_data.timestamp}.csv"
    csv_path = os.path.join(REPORTS_DIR, csv_filename)
    with open(csv_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Video Filename", "Damage Count", "Timestamp"])
        writer.writerow([report_data.video_filename, report_data.damage_count, report_data.timestamp])

    return {"message": "Report generated successfully", "json_path": json_path, "csv_path": csv_path}

@app.get("/list-reports")
async def list_reports():
    reports = os.listdir(REPORTS_DIR)
    return {"reports": reports}