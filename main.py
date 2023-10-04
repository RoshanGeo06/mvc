from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from model import User, Sample, Record

app = FastAPI()

def format_data(user, sample, record):
    return {
        "user_data": {
            "user_id": user.user_id,
            "password": user.password,
            "name": user.name,
            "email": user.email
        },
        "sample_data": {
            "sample_id": sample.sample_id,
            "sample_name": sample.sample_name,
            "description": sample.description,
            "age": sample.age,
            "gender": sample.gender,
            "latitude": sample.latitude,
            "longitude": sample.longitude,
            "marks": sample.marks
        },
        "record_data": {
            "record_id": record.record_id,
            "details": record.details
        }
    }

#end point to display the all table using user_id
def get_user_data(user_id: int, db: Session):
    user_data = (
        db.query(User, Sample, Record)
        .join(Record, User.user_id == Record.user_id)
        .join(Sample, Sample.sample_id == Record.sample_id)
        .filter(User.user_id == user_id)
        .all()
    )
    formatted_data = [format_data(user, sample, record) for user, sample, record in user_data]
    return formatted_data

@app.get("/user/{user_id}")
def read_user_data(user_id: int):
    db = SessionLocal()
    user_data = get_user_data(user_id, db)
    db.close()
    return user_data


#end point to display sample table using user_id
def get_sample_data(user_id: int, db: Session):
    sample_data = (
        db.query(Sample)
        .join(Record, Sample.sample_id == Record.sample_id)
        .filter(Record.user_id == user_id)
        .all()
    )
    return sample_data

@app.get("/sample/{user_id}")
def read_sample_data(user_id: int):
    db = SessionLocal()
    sample_data = get_sample_data(user_id, db)
    db.close()
    return sample_data

def create_user(user_data: dict, db: Session):
    new_user = User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/user")
def add_user(user_data: dict):
    db = SessionLocal()
    try:
        user = create_user(user_data, db)
        db.close()
        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to create user")


# Function to add data to the Sample table
def add_sample_data(sample_data: dict, db: Session):
    sample = Sample(**sample_data)
    db.add(sample)
    db.commit()
    db.refresh(sample)
    return sample

@app.post("/sample/add")
def add_sample(sample_data: dict):
    db = SessionLocal()
    try:
        added_sample = add_sample_data(sample_data, db)
        return {"message": "Sample data added successfully", "sample_data": added_sample}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.post("/add_record/")
def add_record(user_id: int, sample_id: int, details: str):
    db = SessionLocal()
    # Check if the user and sample exist
    user = db.query(User).filter(User.user_id == user_id).first()
    sample = db.query(Sample).filter(Sample.sample_id == sample_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")

    # Create a new record
    new_record = Record(user_id=user_id, sample_id=sample_id, details=details)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    db.close()
    return {"message": "Record added successfully"}
