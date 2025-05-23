package com.azamat.health_monitor_mobile.data.db

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow
import com.azamat.health_monitor_mobile.data.entity.TaskEntity
import com.azamat.health_monitor_mobile.domain.model.TaskStatus
import java.time.LocalDate
import java.time.LocalDateTime

@Dao
interface TaskDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertOne(task: TaskEntity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(tasks: List<TaskEntity>)

    @Query("SELECT * FROM tasks WHERE date(scheduledTime) = :date")
    fun getTasksForDate(date: String): Flow<List<TaskEntity>>

    @Query("SELECT EXISTS (SELECT * FROM tasks WHERE orderId = :orderId AND scheduledTime = :scheduledTime AND type = :type AND title = :title)")
    suspend fun taskExists(orderId: Int, scheduledTime: LocalDateTime, type: String, title: String): Boolean

    @Query("UPDATE tasks SET status = :status WHERE id = :taskId")
    suspend fun updateStatus(taskId: Int, status: TaskStatus)

    @Query("SELECT * FROM tasks WHERE id = :taskId LIMIT 1")
    suspend fun getTaskById(taskId: Int): TaskEntity?

    @Query("SELECT id FROM tasks WHERE orderId = :orderId")
    suspend fun getTaskIdsByOrderId(orderId: Int): List<Int>

    @Query("SELECT orderId FROM tasks WHERE id = :taskId")
    suspend fun getOrderIdByTaskId(taskId: Int): Int?

    @Query("DELETE FROM tasks WHERE orderId = :orderId")
    suspend fun deleteTasksByOrderId(orderId: Int)
}