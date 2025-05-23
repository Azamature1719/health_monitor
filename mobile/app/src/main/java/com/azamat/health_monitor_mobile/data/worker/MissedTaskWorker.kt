import android.content.Context
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.azamat.health_monitor_mobile.data.api.ApiService
import com.azamat.health_monitor_mobile.data.db.OrderDao
import com.azamat.health_monitor_mobile.data.db.TaskDao
import com.azamat.health_monitor_mobile.data.model.ResultDto
import com.azamat.health_monitor_mobile.domain.model.TaskStatus
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class MissedTaskWorker(
    context: Context,
    workerParams: WorkerParameters,
    private val taskDao: TaskDao,
    private val orderDao: OrderDao,
    private val apiService: ApiService
) : CoroutineWorker(context, workerParams) {

    override suspend fun doWork(): Result {
        val taskId = inputData.getInt("taskId", -1)

        return withContext(Dispatchers.IO) {
            val task = taskDao.getTaskById(taskId)
            if (task != null && task.status == TaskStatus.pending) {
                // Обновляем статус задачи на MISSED
                taskDao.updateStatus(taskId, TaskStatus.missed)
                val order = orderDao.getOneById(task.orderId)
                // Отправляем пустой результат на сервер
                try {
                    val resultDto = ResultDto(
                        resultId = 0, // Пустой результат
                        value = 0f, // Пустое значение
                        patientId = 1, // Замените на актуальный ID пациента
                        orderId = task.orderId,
                        typeName = task.type.toString(),
                        title = task.title,
                        unit = order!!.unit.toString(), // Замените на актуальную единицу измерения
                        executionTime = task.scheduledTime.toString(), // Замените на актуальное время выполнения
                        status = TaskStatus.missed.name,
                        doctorId = task.doctorId
                    )
                    apiService.sendResult(resultDto)
                } catch (e: Exception) {
                    return@withContext Result.retry()
                }
            }
            Result.success()
        }
    }
}