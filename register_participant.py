import sqlite3


def register_participant(name, email):
    conn = sqlite3.connect("secretsanta.db")
    cursor = conn.cursor()

    # Check if the participant already exists
    cursor.execute("SELECT id FROM participants WHERE email = ?", (email,))
    existing_participant = cursor.fetchone()

    if existing_participant:
        print("Participant with this email already exists.")
    else:
        # Insert participant into the database
        cursor.execute(
            "INSERT INTO participants (name, email) VALUES (?, ?)", (name, email)
        )
        print("Participant registered successfully!")

    conn.commit()
    conn.close()


# Get participant details
participant_name = input("Enter your name: ")
participant_email = input("Enter your email: ")

# Register participant
register_participant(participant_name, participant_email)
