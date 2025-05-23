import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters

class NotifyWorker(
    context: Context,
    workerParams: WorkerParameters
) : CoroutineWorker(context, workerParams) {

    override suspend fun doWork(): Result {
        // Получаем данные из WorkRequest
        val taskId = inputData.getInt("taskId", -1)
        val message = inputData.getString("message") ?: "Уведомление"

        // Отправляем уведомление
        sendNotification(taskId, message)
        return Result.success()
    }

    private fun sendNotification(taskId: Int, message: String) {
        val notificationManager = applicationContext.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        // Создаём канал уведомлений для Android O и выше
        val channel = NotificationChannel(
            "task_notifications",
            "Task Notifications",
            NotificationManager.IMPORTANCE_HIGH
        )
        notificationManager.createNotificationChannel(channel)

        // Создаём уведомление
        val notification = NotificationCompat.Builder(applicationContext, "task_notifications")
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .setContentTitle("Напоминание о задаче")
            .setContentText(message)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .build()

        // Отправляем уведомление
        notificationManager.notify(taskId, notification)
    }
}