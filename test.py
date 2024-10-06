import unittest
from unittest.mock import patch, mock_open
import os
import shutil

from notes_app import create_note, list_notes, view_note, delete_note

NOTES_DIR = "notes"


class TestNotesApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Create a mock notes directory for testing."""
        if not os.path.exists(NOTES_DIR):
            os.makedirs(NOTES_DIR)

    @classmethod
    def tearDownClass(cls):
        """Remove the mock notes directory after tests."""
        if os.path.exists(NOTES_DIR):
            shutil.rmtree(NOTES_DIR)

    def tearDown(self):
        """Clean up test files after each test."""
        for file in os.listdir(NOTES_DIR):
            os.remove(os.path.join(NOTES_DIR, file))

    @patch("builtins.input", side_effect=["TestNote", "This is a test note."])
    def test_create_note_saves_file(self, mock_input):
        """Test that creating a note saves a file with the correct content."""
        create_note()
        note_path = os.path.join(NOTES_DIR, "TestNote.txt")
        self.assertTrue(os.path.exists(note_path))

        with open(note_path, "r") as file:
            content = file.read()
            self.assertEqual(content, "This is a test note.")

    def test_list_notes_empty(self):
        """Test listing notes when no notes exist."""
        with patch("sys.stdout") as mock_stdout:
            list_notes()
            mock_stdout.write.assert_called_with("No notes found.\n")

    def test_list_notes_with_notes(self):
        """Test listing notes when notes exist."""
        # Create a test note
        with open(os.path.join(NOTES_DIR, "TestNote.txt"), "w") as f:
            f.write("Content")

        with patch("sys.stdout") as mock_stdout:
            list_notes()
            mock_stdout.write.assert_any_call("Available notes:\n")

    @patch("builtins.input", side_effect=["TestNote"])
    def test_view_note_displays_content(self, mock_input):
        """Test viewing a note displays the correct content."""
        # Create a test note
        with open(os.path.join(NOTES_DIR, "TestNote.txt"), "w") as f:
            f.write("Test note content.")

        with patch("sys.stdout") as mock_stdout:
            view_note()
            mock_stdout.write.assert_any_call("Test note content.\n")

    @patch("builtins.input", side_effect=["NonExistentNote"])
    def test_view_note_not_found(self, mock_input):
        """Test viewing a note that doesn't exist."""
        with patch("sys.stdout") as mock_stdout:
            view_note()
            mock_stdout.write.assert_any_call("Note 'NonExistentNote' not found.\n")

    @patch("builtins.input", side_effect=["TestNote"])
    def test_delete_note_removes_file(self, mock_input):
        """Test deleting a note removes the file."""
        # Create a test note
        note_path = os.path.join(NOTES_DIR, "TestNote.txt")
        with open(note_path, "w") as f:
            f.write("Content")

        delete_note()
        self.assertFalse(os.path.exists(note_path))

    @patch("builtins.input", side_effect=["NonExistentNote"])
    def test_delete_note_not_found(self, mock_input):
        """Test trying to delete a non-existent note."""
        with patch("sys.stdout") as mock_stdout:
            delete_note()
            mock_stdout.write.assert_any_call("Note 'NonExistentNote' not found.\n")

    @patch("builtins.input", side_effect=["TestNote", "Another test note"])
    def test_create_multiple_notes(self, mock_input):
        """Test creating multiple notes."""
        create_note()
        create_note()

        notes = os.listdir(NOTES_DIR)
        self.assertEqual(len(notes), 2)
        self.assertIn("TestNote.txt", notes)

    @patch("builtins.input", side_effect=["TestNote"])
    def test_view_note_with_no_content(self, mock_input):
        """Test viewing a note that has no content."""
        note_path = os.path.join(NOTES_DIR, "TestNote.txt")
        with open(note_path, "w") as f:
            pass  # Create an empty note

        with patch("sys.stdout") as mock_stdout:
            view_note()
            mock_stdout.write.assert_any_call("\n--- TestNote ---\n")

    @patch("builtins.input", side_effect=["TestNote"])
    def test_delete_note_and_list(self, mock_input):
        """Test deleting a note and verifying the list of notes is updated."""
        # Create a test note
        note_path = os.path.join(NOTES_DIR, "TestNote.txt")
        with open(note_path, "w") as f:
            f.write("Some content")

        delete_note()

        with patch("sys.stdout") as mock_stdout:
            list_notes()
            mock_stdout.write.assert_any_call("No notes found.\n")


if __name__ == "__main__":
    unittest.main()