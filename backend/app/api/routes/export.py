from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse
from typing import List
import json
import csv
import io
from app.schemas.response import ChannelAnalysis

router = APIRouter(prefix="/api/v1/export", tags=["export"])


@router.post("/csv")
async def export_csv(channels: List[ChannelAnalysis]):
    """
    Export channel analysis results to CSV

    Args:
        channels: List of analyzed channels

    Returns:
        CSV file download
    """
    try:
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow([
            'Channel Name',
            'Channel ID',
            'Channel URL',
            'Tier',
            'Age (days)',
            'Age Description',
            'First Upload Date',
            'Video Count',
            'Subscribers',
            'Total Views',
            'Avg Views Per Video',
            'Has Viral Content',
            'Viral Videos Count'
        ])

        # Write data rows
        for channel in channels:
            writer.writerow([
                channel.channel_name,
                channel.channel_id,
                channel.channel_url,
                channel.tier,
                channel.age_days,
                channel.age_description,
                channel.first_upload_date,
                channel.video_count,
                channel.subscriber_count,
                channel.total_views,
                channel.avg_views_per_video,
                'Yes' if channel.has_viral_content else 'No',
                len(channel.viral_videos)
            ])

        # Get CSV content
        csv_content = output.getvalue()
        output.close()

        # Return as downloadable file
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=niche_analysis.csv"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating CSV: {str(e)}")


@router.post("/json")
async def export_json(channels: List[ChannelAnalysis]):
    """
    Export channel analysis results to JSON

    Args:
        channels: List of analyzed channels

    Returns:
        JSON file download
    """
    try:
        # Convert to dict for JSON serialization
        data = {
            "channels": [channel.model_dump() for channel in channels],
            "total_channels": len(channels),
            "export_date": "2026-01-17"  # Could use datetime.now()
        }

        # Convert to JSON string
        json_content = json.dumps(data, indent=2)

        # Return as downloadable file
        return Response(
            content=json_content,
            media_type="application/json",
            headers={
                "Content-Disposition": "attachment; filename=niche_analysis.json"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating JSON: {str(e)}")
