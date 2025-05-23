package com.azamat.health_monitor_mobile.domain.model

import okhttp3.internal.concurrent.Task
import java.time.LocalDateTime

data class TaskDomain(
    val id: Int,
    val orderId: Int,
    val title: String,
    val scheduledTime: LocalDateTime,
    val status: TaskStatus,
    val type: TaskType,
    val doctorInfo: String
)

fun getTaskTypeByString(typeName: String): TaskType{
   return when(typeName){
        "temperature" -> TaskType.temperature
        "pressure" -> TaskType.pressure
        "saturation" -> TaskType.saturation
        "mood" -> TaskType.mood
        "heart_rate" -> TaskType.heart_rate
        else -> TaskType.other
    }
}

enum class TaskType {
    temperature, pressure, mood, saturation, heart_rate, other
}

enum class TaskStatus {
    pending, done, missed
}
