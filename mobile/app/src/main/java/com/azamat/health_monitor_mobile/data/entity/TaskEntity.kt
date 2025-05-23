package com.azamat.health_monitor_mobile.data.entity

import androidx.room.Entity
import androidx.room.PrimaryKey
import com.azamat.health_monitor_mobile.domain.model.TaskStatus
import com.azamat.health_monitor_mobile.domain.model.TaskType
import java.time.LocalDateTime

@Entity(tableName = "tasks")
data class TaskEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val orderId: Int,
    val title: String,
    val scheduledTime: LocalDateTime,
    val status: TaskStatus,
    val type: TaskType,
    val doctorId: Int,
    val doctorInfo: String
)