package com.azamat.health_monitor_mobile.data.db.di

import android.content.Context
import androidx.room.Room
import com.azamat.health_monitor_mobile.data.db.AppDatabase
import com.azamat.health_monitor_mobile.data.db.Converters
import com.azamat.health_monitor_mobile.data.db.OrderDao
import com.azamat.health_monitor_mobile.data.db.ResultDao
import com.azamat.health_monitor_mobile.data.db.TaskDao
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    @Provides
    @Singleton
    fun provideDatabase(
        @ApplicationContext context: Context
    ): AppDatabase
    {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "health_monitor_db"
        )
            .fallbackToDestructiveMigration()
            .build()
    }

    @Provides
    fun provideOrderDao(db: AppDatabase): OrderDao = db.orderDao()
    @Provides
    fun provideTaskDao(db: AppDatabase): TaskDao = db.taskDao()
    @Provides
    fun provideResultDao(db: AppDatabase): ResultDao = db.resultDao()
}

