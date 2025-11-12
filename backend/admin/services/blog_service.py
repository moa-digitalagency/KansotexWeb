from datetime import datetime
from backend.models import db
from backend.models.blog import BlogArticle
from sqlalchemy import or_


class BlogService:
    """Service class for blog article operations"""
    
    @staticmethod
    def get_all_articles(published_only=False, limit=None):
        """Get all blog articles"""
        query = BlogArticle.query
        
        if published_only:
            query = query.filter_by(is_published=True)
        
        query = query.order_by(BlogArticle.published_at.desc(), BlogArticle.created_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    @staticmethod
    def get_article_by_id(article_id):
        """Get a single article by ID"""
        return BlogArticle.query.get(article_id)
    
    @staticmethod
    def get_article_by_slug(slug):
        """Get a single article by slug"""
        return BlogArticle.query.filter_by(slug=slug).first()
    
    @staticmethod
    def create_article(data):
        """Create a new blog article"""
        article = BlogArticle(
            slug=data.get('slug'),
            title_fr=data.get('title_fr'),
            title_en=data.get('title_en'),
            excerpt_fr=data.get('excerpt_fr'),
            excerpt_en=data.get('excerpt_en'),
            content_fr=data.get('content_fr'),
            content_en=data.get('content_en'),
            featured_image_id=data.get('featured_image_id'),
            author_name=data.get('author_name'),
            category_fr=data.get('category_fr'),
            category_en=data.get('category_en'),
            tags_fr=data.get('tags_fr'),
            tags_en=data.get('tags_en'),
            meta_title_fr=data.get('meta_title_fr'),
            meta_title_en=data.get('meta_title_en'),
            meta_description_fr=data.get('meta_description_fr'),
            meta_description_en=data.get('meta_description_en'),
            meta_keywords_fr=data.get('meta_keywords_fr'),
            meta_keywords_en=data.get('meta_keywords_en'),
            is_published=data.get('is_published', False)
        )
        
        if article.is_published and not article.published_at:
            article.published_at = datetime.utcnow()
        
        db.session.add(article)
        db.session.commit()
        return article
    
    @staticmethod
    def update_article(article_id, data):
        """Update an existing article"""
        article = BlogArticle.query.get(article_id)
        if not article:
            return None
        
        # Update fields
        for field in ['slug', 'title_fr', 'title_en', 'excerpt_fr', 'excerpt_en',
                      'content_fr', 'content_en', 'featured_image_id', 'author_name',
                      'category_fr', 'category_en', 'tags_fr', 'tags_en',
                      'meta_title_fr', 'meta_title_en', 'meta_description_fr',
                      'meta_description_en', 'meta_keywords_fr', 'meta_keywords_en']:
            if field in data:
                setattr(article, field, data[field])
        
        # Handle publication status
        if 'is_published' in data:
            was_published = article.is_published
            article.is_published = data['is_published']
            
            # Set published_at when first published
            if article.is_published and not was_published:
                article.published_at = datetime.utcnow()
        
        db.session.commit()
        return article
    
    @staticmethod
    def delete_article(article_id):
        """Delete an article"""
        article = BlogArticle.query.get(article_id)
        if not article:
            return False
        
        db.session.delete(article)
        db.session.commit()
        return True
    
    @staticmethod
    def increment_view_count(article_id):
        """Increment article view count"""
        article = BlogArticle.query.get(article_id)
        if article:
            article.view_count += 1
            db.session.commit()
        return article
    
    @staticmethod
    def get_related_articles(article, limit=3):
        """Get related articles based on category and tags"""
        if not article:
            return []
        
        # Get articles with same category or overlapping tags
        related = BlogArticle.query.filter(
            BlogArticle.id != article.id,
            BlogArticle.is_published == True,
            or_(
                BlogArticle.category_fr == article.category_fr,
                BlogArticle.category_en == article.category_en
            )
        ).limit(limit).all()
        
        return related
    
    @staticmethod
    def search_articles(query_text, lang='fr', limit=10):
        """Search articles by title or content"""
        if lang == 'fr':
            results = BlogArticle.query.filter(
                BlogArticle.is_published == True,
                or_(
                    BlogArticle.title_fr.ilike(f'%{query_text}%'),
                    BlogArticle.content_fr.ilike(f'%{query_text}%'),
                    BlogArticle.excerpt_fr.ilike(f'%{query_text}%')
                )
            ).limit(limit).all()
        else:
            results = BlogArticle.query.filter(
                BlogArticle.is_published == True,
                or_(
                    BlogArticle.title_en.ilike(f'%{query_text}%'),
                    BlogArticle.content_en.ilike(f'%{query_text}%'),
                    BlogArticle.excerpt_en.ilike(f'%{query_text}%')
                )
            ).limit(limit).all()
        
        return results


blog_service = BlogService()
