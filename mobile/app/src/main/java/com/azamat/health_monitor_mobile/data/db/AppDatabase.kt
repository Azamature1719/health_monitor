package com.azamat.health_monitor_mobile.data.db

import androidx.room.Database
import androidx.room.RoomDatabase
import androidx.room.TypeConverters
import com.azamat.health_monitor_mobile.data.entity.OrderEntity
import com.azamat.health_monitor_mobile.data.entity.TaskEntity
import com.azamat.health_monitor_mobile.data.db.TaskDao
import com.azamat.health_monitor_mobile.data.entity.ResultEntity

@Database(
    entities = [
        OrderEntity::class,
        TaskEntity::class,
        ResultEntity::class],
    version = 5
)

@TypeConverters(Converters::class)
abstract class AppDatabase: RoomDatabase(){
    abstract fun orderDao(): OrderDao
    abstract fun taskDao(): TaskDao
    abstract fun resultDao(): ResultDao
}