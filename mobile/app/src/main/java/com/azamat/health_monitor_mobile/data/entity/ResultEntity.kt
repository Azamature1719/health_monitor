package com.azamat.health_monitor_mobile.data.entity

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.sql.Timestamp
import java.time.LocalDateTime

@Entity(tableName = "results")
data class ResultEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val taskId: Int,
    val value: Float,
    val timestamp: LocalDateTime = LocalDateTime.now()
)