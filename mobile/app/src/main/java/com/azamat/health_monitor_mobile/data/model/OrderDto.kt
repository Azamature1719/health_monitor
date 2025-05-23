package com.azamat.health_monitor_mobile.data.model

import com.azamat.health_monitor_mobile.data.entity.OrderEntity

data class OrderDto(
    val orderId: Int,
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
){
    fun toEntity(): OrderEntity {
        return OrderEntity(
            orderId = orderId,
            typeName = typeName,
            title = title,
            unit = unit,
            startDate = startDate,
            endDate = endDate,
            executionTimes = executionTimes,
            description = description,
            status = status,
            doctorId = doctorId,
            doctorInfo = doctorInfo
        )
    }
}