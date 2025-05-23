package com.azamat.health_monitor_mobile.domain.mappers

import com.azamat.health_monitor_mobile.data.entity.TaskEntity
import com.azamat.health_monitor_mobile.domain.model.TaskDomain

fun TaskEntity.toDomain(): TaskDomain{
    return TaskDomain(
        id = this.id,
        orderId = this.orderId,
        title = this.title,
        scheduledTime = this.scheduledTime,
        status = this.status,
        type = this.type,
        doctorInfo = this.doctorInfo
    )
}