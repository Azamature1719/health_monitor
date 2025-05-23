package com.azamat.health_monitor_mobile.data.worker

import NotifyWorker
import android.content.Context
import androidx.work.Data
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.WorkManager
import com.azamat.health_monitor_mobile.data.entity.TaskEntity
import com.azamat.health_monitor_mobile.domain.model.TaskType
import java.time.ZoneOffset
import java.util.concurrent.TimeUnit

class NotificationScheduler(private val context: Context) {

    fun scheduleTaskNotifications(task: TaskEntity) {
        // Создание WorkRequest для основного уведомления
        val notificationData = Data.Builder()
            .putInt("taskId", task.id)
            .putString("message", "Время выполнить задачу: ${task.title}")
            .build()

        val notificationWorkRequest = OneTimeWorkRequestBuilder<NotifyWorker>()
            .setInitialDelay(calculateDelay(task.scheduledTime.toEpochSecond(ZoneOffset.UTC)), TimeUnit.MILLISECONDS)
            .setInputData(notificationData)
            .build()

        WorkManager.getInstance(context).enqueue(notificationWorkRequest)

        // Если задача требует предварительного уведомления

        if (task.type == TaskType.heart_rate || task.type == TaskType.saturation) {

            val message: String = when(task.type){
                TaskType.saturation -> "Через 10 минут будет измерена сатурация кислорода в крови, не снимайте устройство!"
                TaskType.heart_rate -> "Через 10 минут будет измерен сердечный ритм, не снимайте устройство!"
                else -> {""}
            }
            val preNotificationData = Data.Builder()
                .putInt("taskId", task.id)
                .putString("message", message)
                .build()

            val preNotificationWorkRequest = OneTimeWorkRequestBuilder<NotifyWorker>()
                .setInitialDelay(calculateDelay(task.scheduledTime.toEpochSecond(ZoneOffset.UTC) - 10 * 60), TimeUnit.SECONDS)
                .setInputData(preNotificationData)
                .build()

            WorkManager.getInstance(context).enqueue(preNotificationWorkRequest)
        }
    }

    private fun calculateDelay(taskTime: Long): Long {
        val currentTime = System.currentTimeMillis()
        return taskTime - currentTime
    }
}