package com.azamat.health_monitor_mobile.data.model

import java.time.LocalDateTime

data class ResultDto(
    val resultId: Int,
    val orderId: Int,
    val patientId: Int,
    val doctorId: Int,
    val typeName: String,
    val title: String,
    val unit: String,
    val executionTime: String,
    val value: Float,
    val status: String
)

