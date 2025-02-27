class MultiDBRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'customer':
            return 'default'  # MySQL
        elif model._meta.db_alias == 'mongodb':
            return 'mongodb'  # MongoDB
        elif model._meta.db_alias == 'postgresql':
            return 'postgresql'  # PostgreSQL
        return None

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'customer':
            return db == 'default'
        elif db == 'mongodb':
            return False  
        elif db == 'postgresql':
            return True
        return None
