from models import ChatbotSettings, ChatMessage, AllowList, AllowedEmailEndings, BlockList, db
from abilities import llm
from flask import Response
from datetime import datetime, timedelta
from flask import render_template, jsonify, url_for, request, redirect, session, flash
from flask import current_app as app
import logging
from datetime import datetime

def register_routes(app):
    # Main routes
    @app.route("/")
    def home_route():
        settings = ChatbotSettings.query.first()
        if not settings:
            settings = ChatbotSettings()
            db.session.add(settings)
            db.session.commit()
        return render_template("home.html", title="Home", settings=settings)

    @app.route("/company-admins")
    def company_admins_route():
        allowed_emails = AllowList.query.all()
        allowed_endings = AllowedEmailEndings.query.all()
        blocked_emails = BlockList.query.all()
        
        for email in allowed_emails:
            email.is_blocked = any(blocked.email == email.email for blocked in blocked_emails)
            email.role = "Owner" if email.id == 1 else email.role
        
        return render_template("company_admins.html", title="Company Admins", allowed_emails=allowed_emails, allowed_endings=allowed_endings)

    @app.route("/simulator")
    def ai_chat_route():
        user_id = session['user']['email']
        chat_history = ChatMessage.query.filter_by(user_id=user_id).order_by(ChatMessage.timestamp).all()
        return render_template("ai_chat.html", title="AI Chat Simulator", chat_history=chat_history)

    # Settings API routes
    @app.route("/api/update_settings", methods=["POST"])
    def update_settings():
        try:
            settings = ChatbotSettings.query.first()
            if not settings:
                settings = ChatbotSettings()
                db.session.add(settings)
            
            settings.moderation_prompt = request.form.get("moderation_prompt", "")
            settings.model_selection = request.form.get("model_selection", "gpt-4o")
            settings.temperature = float(request.form.get("temperature", 0.7))
            
            db.session.commit()
            return jsonify({"status": "success", "message": "Settings updated successfully"})
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error updating settings: {str(e)}")
            return jsonify({"status": "error", "message": "An error occurred while updating settings"}), 500

    # Admin management API routes
    @app.route("/api/company_admins/create", methods=["POST"])
    def api_create_company_admin():
        email = request.json.get('email')
        if not email:
            return jsonify({"status": "error", "message": "Email is required"}), 400
        
        try:
            new_email = AllowList(email=email)
            db.session.add(new_email)
            db.session.commit()
            return jsonify({"status": "success", "message": "Email added to allow list successfully"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500
    
    @app.route("/api/allowed_email_endings/create", methods=["POST"])
    def api_create_allowed_email_ending():
        email_ending = request.json.get('email_ending')
        if not email_ending:
            return jsonify({"status": "error", "message": "Email ending is required"}), 400
        # Remove '@' if it's included in the email ending
        email_ending = email_ending.lstrip('@')
        
        try:
            new_ending = AllowedEmailEndings(email_ending=email_ending)
            db.session.add(new_ending)
            db.session.commit()
            return jsonify({"status": "success", "message": "Email ending added successfully"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500
            
    @app.route("/api/delete_admin/<int:admin_id>", methods=["DELETE"])
    def delete_admin(admin_id):
        try:
            if admin_id == 1:
                return jsonify({"status": "error", "message": "You are not allowed to delete the super admin."}), 403
            admin = AllowList.query.get(admin_id)
            if admin:
                if admin.email == session['user']['email']:
                    return jsonify({"status": "error", "message": "You are not allowed to delete yourself as an admin."}), 403
                db.session.delete(admin)
                db.session.commit()
                return jsonify({"status": "success", "message": "Admin deleted successfully"})
            else:
                return jsonify({"status": "error", "message": "Admin not found"}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500
        
    @app.route("/api/block_admin/<int:admin_id>", methods=["POST"])
    def block_admin(admin_id):
        try:
            admin = AllowList.query.get(admin_id)
            if admin:
                if admin.email == session['user']['email']:
                    return jsonify({"status": "error", "message": "You cannot block yourself"}), 403
                blocked = BlockList(email=admin.email)
                db.session.add(blocked)
                db.session.commit()
                return jsonify({"status": "success", "message": "Admin blocked successfully"})
            else:
                return jsonify({"status": "error", "message": "Admin not found"}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500
    
    @app.route("/api/unblock_admin/<int:admin_id>", methods=["POST"])
    def unblock_admin(admin_id):
        try:
            admin = AllowList.query.get(admin_id)
            if admin:
                blocked = BlockList.query.filter_by(email=admin.email).first()
                if blocked:
                    db.session.delete(blocked)
                    db.session.commit()
                    return jsonify({"status": "success", "message": "Admin unblocked successfully"})
                else:
                    return jsonify({"status": "error", "message": "Admin was not blocked"}), 400
            else:
                return jsonify({"status": "error", "message": "Admin not found"}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route("/api/delete_email_ending/<int:ending_id>", methods=["DELETE"])
    def delete_email_ending(ending_id):
        try:
            ending = AllowedEmailEndings.query.get(ending_id)
            if ending:
                # Get all admins with this email ending
                admins_to_remove = AllowList.query.filter(
                    AllowList.email.like(f"%@{ending.email_ending}"),
                    AllowList.id != 1  # Exclude the owner (ID 1)
                ).all()
                
                # Delete the admins
                removed_count = len(admins_to_remove)
                for admin in admins_to_remove:
                    db.session.delete(admin)
                
                # Delete the email ending
                db.session.delete(ending)
                db.session.commit()
                
                message = f"Email ending deleted successfully. {removed_count} admin{'s' if removed_count != 1 else ''} removed."
                return jsonify({"status": "success", "message": message})
            else:
                return jsonify({"status": "error", "message": "Email ending not found"}), 404
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error deleting email ending: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500

    # Chat API routes
    @app.route("/api/chat", methods=["POST"])
    def chat():
        user_message = request.json.get("message")
        user_id = session['user']['email']
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # Get chatbot settings
        settings = ChatbotSettings.get_settings()

        try:
            # Get chat history
            chat_history = ChatMessage.query.filter_by(user_id=user_id).order_by(ChatMessage.timestamp).limit(10).all()
            chat_context = "\n".join([f"{'AI' if msg.is_ai else 'User'}: {msg.message}" for msg in chat_history])

            # Prepare chat instructions
            chat_instructions = f"""
            Instructions for AI Assistant:
            {settings.moderation_prompt}

            Please provide a helpful and informative response to the user's message.
            """

            response = llm(
                prompt=f"{chat_instructions}\n\n{chat_context}\nUser: {user_message}\nAI:",
                response_schema={
                    "type": "object",
                    "properties": {
                        "response": {"type": "string"}
                    },
                    "required": ["response"]
                },
                image_url=None,
                model=settings.model_selection,
                temperature=settings.temperature
            )

            ai_response = response["response"]

            # Save user message
            user_chat = ChatMessage(
                user_id=user_id,
                message=user_message,
                is_ai=False,
                model=settings.model_selection
            )
            db.session.add(user_chat)

            # Save AI message
            ai_chat = ChatMessage(
                user_id=user_id,
                message=ai_response,
                is_ai=True,
                model=settings.model_selection
            )
            db.session.add(ai_chat)
            db.session.commit()

            return jsonify({
                "response": ai_response,
                "model": settings.model_selection
            })
        except Exception as e:
            app.logger.error(f"Error in chat API: {str(e)}")
            return jsonify({"error": "An error occurred while processing your request"}), 500

    @app.route("/api/clear_chats", methods=["POST"])
    def clear_chats():
        try:
            user_id = session['user']['email']
            ChatMessage.query.filter_by(user_id=user_id).delete()
            db.session.commit()
            return jsonify({"status": "success", "message": "All chats cleared successfully"})
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error clearing chats: {str(e)}")
            return jsonify({"status": "error", "message": "An error occurred while clearing chats"}), 500
    
    # Chat History routes
    @app.route("/api/chat_history/search", methods=["POST"])
    def search_chat_history():
        try:
            user_id = session['user']['email']
            search = request.json.get('search', '')
            date_filter = request.json.get('date_filter', '')
            model_filter = request.json.get('model_filter', '')
            
            query = ChatMessage.query.filter_by(user_id=user_id)
            
            if search:
                query = query.filter(ChatMessage.message.ilike(f'%{search}%'))
            
            if date_filter:
                today = datetime.now().date()
                if date_filter == 'today':
                    query = query.filter(db.func.date(ChatMessage.timestamp) == today)
                elif date_filter == 'week':
                    week_ago = today - timedelta(days=7)
                    query = query.filter(db.func.date(ChatMessage.timestamp) >= week_ago)
                elif date_filter == 'month':
                    month_ago = today - timedelta(days=30)
                    query = query.filter(db.func.date(ChatMessage.timestamp) >= month_ago)
            
            if model_filter:
                query = query.filter(ChatMessage.model == model_filter)
            
            messages = query.order_by(ChatMessage.timestamp.desc()).all()
            return jsonify({"status": "success", "messages": [
                {
                    "id": msg.id,
                    "message": msg.message,
                    "is_ai": msg.is_ai,
                    "timestamp": msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    "model": msg.model
                } for msg in messages
            ]})
        except Exception as e:
            app.logger.error(f"Error searching chat history: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500
    
    @app.route("/api/chat_history/export", methods=["GET"])
    def export_chat_history():
        try:
            user_id = session['user']['email']
            messages = ChatMessage.query.filter_by(user_id=user_id).order_by(ChatMessage.timestamp).all()
            
            # Create CSV content
            csv_content = "Timestamp,Sender,Model,Message\n"
            for msg in messages:
                timestamp = msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                sender = "AI" if msg.is_ai else "User"
                model = msg.model if msg.is_ai else ""
                # Escape quotes in message
                message = msg.message.replace('"', '""')
                csv_content += f'"{timestamp}","{sender}","{model}","{message}"\n'
            
            from flask import Response
            return Response(
                csv_content,
                mimetype="text/csv",
                headers={"Content-Disposition": "attachment;filename=chat_history.csv"}
            )
        except Exception as e:
            app.logger.error(f"Error exporting chat history: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500

    # Authentication routes
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for('home_route'))

    # Error handlers
    @app.errorhandler(401)
    def unauthorized(e):
        return render_template('unauthorized.html'), 401

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500