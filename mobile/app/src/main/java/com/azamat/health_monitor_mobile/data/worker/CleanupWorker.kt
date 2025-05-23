import android.content.Context
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.azamat.health_monitor_mobile.data.db.OrderDao
import com.azamat.health_monitor_mobile.data.db.TaskDao
import com.azamat.health_monitor_mobile.data.db.ResultDao
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.time.LocalDate

class CleanupWorker(
    context: Context,
    workerParams: WorkerParameters,
    private val orderDao: OrderDao,
    private val taskDao: TaskDao,
    private val resultDao: ResultDao
) : CoroutineWorker(context, workerParams) {

    override suspend fun doWork(): Result {
        return withContext(Dispatchers.IO) {
            try {
                val today = LocalDate.now()
                val expiredOrders = orderDao.getExpiredOrders(today.toString())
                expiredOrders.forEach { order ->
                    val taskIds = taskDao.getTaskIdsByOrderId(order.orderId)
                    taskIds.forEach{ taskId ->
                        resultDao.deleteResultsByTaskId(taskId)
                    }
                    taskDao.deleteTasksByOrderId(order.orderId)
                    orderDao.deleteOrder(order.orderId)
                }

                Result.success()
            } catch (e: Exception) {
                Result.retry()
            }
        }
    }
}