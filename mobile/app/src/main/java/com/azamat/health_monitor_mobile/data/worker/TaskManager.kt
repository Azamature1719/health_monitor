package com.azamat.health_monitor_mobile.data.worker

import MissedTaskWorker
import android.content.Context
import com.azamat.health_monitor_mobile.data.worker.NotificationScheduler
import androidx.work.*
import com.azamat.health_monitor_mobile.data.entity.TaskEntity
import java.time.Duration
import java.time.LocalDateTime
import java.util.concurrent.TimeUnit

object TaskScheduler {

    fun scheduleTask(
        context: Context,
        task: TaskEntity
    ) {
        // 1. Запланировать уведомления
        val notificationScheduler = NotificationScheduler(context)
        notificationScheduler.scheduleTaskNotifications(task)

        // 2. Запланировать изменение статуса на MISSED через 1 час после taskTime
        val now = LocalDateTime.now()
        val deadline = task.scheduledTime.plusHours(1)
        val delayMillis = Duration.between(now, deadline).toMillis()

        val missedWorkRequest = OneTimeWorkRequestBuilder<MissedTaskWorker>()
            .setInitialDelay(delayMillis, TimeUnit.MILLISECONDS)
            .setInputData(workDataOf("taskId" to task.id))
            .addTag("missed_${task.id}")
            .build()

        WorkManager.getInstance(context).enqueueUniqueWork(
            "missed_task_${task.id}",
            ExistingWorkPolicy.REPLACE,
            missedWorkRequest
        )
    }

    fun scheduleTasks(
        context: Context,
        tasks: List<TaskEntity>
    ) {
        tasks.forEach { task ->
            scheduleTask(context, task)
        }
    }
}