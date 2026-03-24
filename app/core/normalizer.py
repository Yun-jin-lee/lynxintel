from app.core.models import ProbeResult


def normalize_probe_result(result: ProbeResult) -> dict:
    return {
        "status": result.status,
        "input_type": result.input_type,
        "value": result.value,
        "adapter": result.adapter,
        "message": result.message,
        "btih": result.btih,
        "metadata_only": result.metadata_only,
        "files": result.files,
        "source": result.source,
        "extra": result.extra,
    }