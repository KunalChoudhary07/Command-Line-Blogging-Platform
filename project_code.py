import mysql.connector
import hashlib
import getpass # For securely typing passwords

# --- DATABASE CONFIGURATION ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'blog_db'
}

# Global dictionary to store logged-in user's info
current_user = {"id": None, "username": None}

# --- HELPER & UTILITY FUNCTIONS ---

def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    """Establishes and returns a database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Database Connection Error: {err}")
        return None

# --- USER MANAGEMENT ---

def register_user():
    print("\n--- Register a New User ---")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    
    conn = get_db_connection()
    if not conn: return

    try:
        cursor = conn.cursor()
        sql = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
        cursor.execute(sql, (username, hash_password(password)))
        conn.commit()
        print("User registered successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}") # Could be a duplicate username
    finally:
        cursor.close()
        conn.close()

def login_user():
    print("\n--- User Login ---")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    
    conn = get_db_connection()
    if not conn: return
    
    try:
        cursor = conn.cursor()
        sql = "SELECT user_id, username, password_hash FROM users WHERE username = %s"
        cursor.execute(sql, (username,))
        user_record = cursor.fetchone()
        
        if user_record and user_record[2] == hash_password(password):
            current_user["id"] = user_record[0]
            current_user["username"] = user_record[1]
            print(f"\n Welcome, {current_user['username']}!")
            main_menu() # Go to the main application menu
        else:
            print("Invalid username or password.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# --- POST MANAGEMENT ---

def create_post():
    print("\n--- Create a New Post ---")
    title = input("Enter post title: ")
    content = input("Enter post content: \n")
    
    conn = get_db_connection()
    if not conn: return
    
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO posts (author_id, title, content) VALUES (%s, %s, %s)"
        cursor.execute(sql, (current_user["id"], title, content))
        conn.commit()
        print("Post created successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def edit_post():
    print("\n--- Edit a Post ---")
    list_all_posts()
    try:
        post_id = int(input("Enter the ID of the post you want to edit: "))
    except ValueError:
        print("Invalid ID.")
        return

    conn = get_db_connection()
    if not conn: return
    
    try:
        cursor = conn.cursor()
        # Verify the logged-in user is the author of the post
        sql_verify = "SELECT author_id FROM posts WHERE post_id = %s"
        cursor.execute(sql_verify, (post_id,))
        post = cursor.fetchone()

        if not post or post[0] != current_user["id"]:
            print("You can only edit your own posts.")
            return

        print("Enter new title (leave blank to keep current):")
        new_title = input("> ")
        print("Enter new content (leave blank to keep current):")
        new_content = input("> ")

        if new_title:
            cursor.execute("UPDATE posts SET title = %s WHERE post_id = %s", (new_title, post_id))
        if new_content:
            cursor.execute("UPDATE posts SET content = %s WHERE post_id = %s", (new_content, post_id))
        
        conn.commit()
        print("✅ Post updated successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def delete_post():
    print("\n--- Delete a Post ---")
    list_all_posts()
    try:
        post_id = int(input("Enter the ID of the post you want to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    conn = get_db_connection()
    if not conn: return
    
    try:
        cursor = conn.cursor()
        # Verify ownership before deleting
        sql_verify = "SELECT author_id FROM posts WHERE post_id = %s"
        cursor.execute(sql_verify, (post_id,))
        post = cursor.fetchone()

        if not post or post[0] != current_user["id"]:
            print("You can only delete your own posts.")
            return

        cursor.execute("DELETE FROM posts WHERE post_id = %s", (post_id,))
        conn.commit()
        print("✅ Post deleted successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# --- VIEWING & INTERACTION ---

def list_all_posts():
    print("\n--- All Blog Posts ---")
    conn = get_db_connection()
    if not conn: return
    
    try:
        cursor = conn.cursor()
        sql = """
            SELECT p.post_id, p.title, u.username 
            FROM posts p JOIN users u ON p.author_id = u.user_id 
            ORDER BY p.created_at DESC
        """
        cursor.execute(sql)
        posts = cursor.fetchall()
        
        if not posts:
            print("No posts found.")
            return
        
        for post in posts:
            print(f"[{post[0]}] {post[1]} (by {post[2]})")
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def view_post_details():
    print("\n--- View Post Details ---")
    list_all_posts()
    try:
        post_id = int(input("Enter the ID of the post you want to view: "))
    except ValueError:
        print("Invalid ID.")
        return

    conn = get_db_connection()
    if not conn: return
    
    try:
        cursor = conn.cursor(dictionary=True) # Fetch as dictionary
        # Get post details
        sql_post = """
            SELECT p.title, p.content, u.username
            FROM posts p JOIN users u ON p.author_id = u.user_id
            WHERE p.post_id = %s
        """
        cursor.execute(sql_post, (post_id,))
        post = cursor.fetchone()
        
        if not post:
            print("Post not found.")
            return
            
        print("\n" + "="*50)
        print(f"Title: {post['title']}")
        print(f"Author: {post['username']}")
        print("-" * 50)
        print(post['content'])
        print("="*50)

        # Get categories
        sql_cats = """
            SELECT c.category_name FROM categories c
            JOIN post_categories pc ON c.category_id = pc.category_id
            WHERE pc.post_id = %s
        """
        cursor.execute(sql_cats, (post_id,))
        categories = [row['category_name'] for row in cursor.fetchall()]
        if categories:
            print(f"Categories: {', '.join(categories)}")
        
        # Get comments
        print("\n--- Comments ---")
        sql_comments = """
            SELECT c.comment_text, u.username FROM comments c
            JOIN users u ON c.user_id = u.user_id
            WHERE c.post_id = %s AND c.status = 'approved'
        """
        cursor.execute(sql_comments, (post_id,))
        comments = cursor.fetchall()
        
        if not comments:
            print("No comments yet.")
        else:
            for comment in comments:
                print(f"{comment['username']}: {comment['comment_text']}")

        # Interaction menu
        while True:
            print("\nOptions: [1] Add Comment, [2] Manage Categories, [0] Back to Main Menu")
            choice = input("> ")
            if choice == '1':
                add_comment(post_id)
            elif choice == '2':
                manage_categories(post_id)
            elif choice == '0':
                break
                
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def add_comment(post_id):
    comment_text = input("Write your comment: ")
    conn = get_db_connection()
    if not conn: return

    try:
        cursor = conn.cursor()
        sql = "INSERT INTO comments (post_id, user_id, comment_text) VALUES (%s, %s, %s)"
        cursor.execute(sql, (post_id, current_user["id"], comment_text))
        conn.commit()
        print("Comment added!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def manage_categories(post_id):
    conn = get_db_connection()
    if not conn: return

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categories")
        all_categories = cursor.fetchall()

        print("\n--- Manage Categories ---")
        for cat in all_categories:
            print(f"[{cat['category_id']}] {cat['category_name']}")
        
        cat_id = int(input("Enter Category ID to add to this post (or 0 to cancel): "))
        if cat_id == 0: return

        # Check if category exists
        if any(c['category_id'] == cat_id for c in all_categories):
            sql = "INSERT INTO post_categories (post_id, category_id) VALUES (%s, %s)"
            cursor.execute(sql, (post_id, cat_id))
            conn.commit()
            print("Category added!")
        else:
            print("Invalid category ID.")

    except (ValueError, mysql.connector.Error) as err:
        # Catch duplicate key errors if category is already assigned
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# --- MENUS ---

def main_menu():
    while True:
        print("\n===== Main Menu =====")
        print(f"Logged in as: {current_user['username']}")
        print("1. Create a Post")
        print("2. List All Posts")
        print("3. View Post Details (and comment/categorize)")
        print("4. Edit a Post (Yours only)")
        print("5. Delete a Post (Yours only)")
        print("6. Logout")
        
        choice = input("> ")
        if choice == '1': create_post()
        elif choice == '2': list_all_posts()
        elif choice == '3': view_post_details()
        elif choice == '4': edit_post()
        elif choice == '5': delete_post()
        elif choice == '6':
            current_user["id"] = None
            current_user["username"] = None
            print("You have been logged out.")
            break
        else:
            print("Invalid choice.")

def start_screen():
    while True:
        print("\n===== Welcome to the Blog CLI =====")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("> ")
        if choice == '1': login_user()
        elif choice == '2': register_user()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

# --- START THE APPLICATION ---
if __name__ == "__main__":
    start_screen()