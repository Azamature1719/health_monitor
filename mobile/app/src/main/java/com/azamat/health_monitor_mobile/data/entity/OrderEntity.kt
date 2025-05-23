package com.azamat.health_monitor_mobile.data.entity

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.time.LocalDate
import java.time.LocalTime

@Entity(tableName = "orders")
data class OrderEntity (
    @PrimaryKey val orderId: Int,
    val typeName: String,
    val title: String,
    val unit: String,
    val startDate: String,
    val endDate: String,
    val executionTimes: List<String>,
    val description: String,
    val status: String,
    val doctorId: Int,
    val doctorInfo: String
    )