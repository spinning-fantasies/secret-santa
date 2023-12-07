import sqlite3
import random


def assign_recipients():
    conn = sqlite3.connect("secretsanta.db")
    cursor = conn.cursor()

    # Add the 'assigned_recipient' column if not present
    cursor.execute(
        """
        PRAGMA table_info(participants)
    """
    )
    columns = cursor.fetchall()
    if not any(col[1] == "assigned_recipient" for col in columns):
        cursor.execute(
            """
            ALTER TABLE participants
            ADD COLUMN assigned_recipient INTEGER DEFAULT 0
        """
        )

    # Fetch all participants without assigned recipients
    cursor.execute(
        "SELECT id, name, email FROM participants WHERE assigned_recipient = 0"
    )
    participants = cursor.fetchall()

    # Shuffle participants to randomize recipient assignment
    random.shuffle(participants)

    # Assign recipients to each participant
    for i in range(len(participants)):
        recipient_index = (i + 1) % len(participants)  # Ensure no one gets themselves
        participant_id, participant_name, participant_email = participants[i]
        recipient_id, recipient_name, recipient_email = participants[recipient_index]

        # Update the database with the assigned recipient
        cursor.execute(
            "UPDATE participants SET assigned_recipient = ? WHERE id = ?",
            (
                recipient_id,
                participant_id,
            ),
        )

        # Print the assignment (for demonstration purposes)
        print(f"{participant_name} (Email: {participant_email}) -> {recipient_name}")

    conn.commit()
    conn.close()


# Call the function to assign recipients
assign_recipients()
