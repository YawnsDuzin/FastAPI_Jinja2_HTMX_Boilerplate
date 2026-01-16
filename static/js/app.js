/**
 * Main Application JavaScript
 *
 * HTMX와 Alpine.js를 사용하므로 최소한의 JavaScript만 포함합니다.
 */

// Toast Handler (Alpine.js component)
function toastHandler() {
    return {
        toasts: [],

        show(detail) {
            const toast = {
                id: Date.now(),
                type: detail.type || 'info',
                message: detail.message || '알림',
            };

            this.toasts.push(toast);

            // 5초 후 자동 제거
            setTimeout(() => {
                this.remove(toast.id);
            }, 5000);
        },

        remove(id) {
            this.toasts = this.toasts.filter(t => t.id !== id);
        }
    };
}

// HTMX Configuration
document.addEventListener('DOMContentLoaded', () => {
    // HTMX 에러 핸들링
    document.body.addEventListener('htmx:responseError', (event) => {
        console.error('HTMX Error:', event.detail);

        // 401 에러 시 로그인 페이지로 리다이렉트
        if (event.detail.xhr.status === 401) {
            window.location.href = '/login';
        }

        // 토스트 메시지 표시
        const errorMessage = event.detail.xhr.responseText || '오류가 발생했습니다.';
        htmx.trigger('#toast-container', 'showToast', {
            type: 'error',
            message: errorMessage
        });
    });

    // HTMX 요청 전처리
    document.body.addEventListener('htmx:configRequest', (event) => {
        // JSON 요청인 경우 Content-Type 설정
        if (event.detail.headers['Content-Type'] === undefined) {
            // form 데이터는 자동으로 처리됨
        }
    });

    // HX-Trigger 이벤트 처리
    document.body.addEventListener('htmx:afterRequest', (event) => {
        const triggerHeader = event.detail.xhr.getResponseHeader('HX-Trigger');
        if (triggerHeader) {
            try {
                const triggers = JSON.parse(triggerHeader);

                // showToast 트리거 처리
                if (triggers.showToast) {
                    htmx.trigger('#toast-container', 'showToast', triggers.showToast);
                }

                // closeModal 트리거 처리
                if (triggers.closeModal) {
                    htmx.trigger(document.body, 'closeModal');
                }

                // refreshList 트리거 처리
                if (triggers.refreshList) {
                    htmx.trigger('#items-list', 'refresh');
                }
            } catch (e) {
                // 단순 문자열 트리거
            }
        }
    });
});

// Dark mode initialization
(function () {
    // 시스템 설정 확인
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const storedMode = localStorage.getItem('darkMode');

    if (storedMode === 'true' || (storedMode === null && prefersDark)) {
        document.documentElement.classList.add('dark');
    }
})();

// Utility functions
const Utils = {
    // 디바운스
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // 쓰로틀
    throttle(func, limit) {
        let inThrottle;
        return function executedFunction(...args) {
            if (!inThrottle) {
                func(...args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },

    // 날짜 포맷팅
    formatDate(date, format = 'YYYY-MM-DD') {
        const d = new Date(date);
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        const hours = String(d.getHours()).padStart(2, '0');
        const minutes = String(d.getMinutes()).padStart(2, '0');

        return format
            .replace('YYYY', year)
            .replace('MM', month)
            .replace('DD', day)
            .replace('HH', hours)
            .replace('mm', minutes);
    },

    // 클립보드 복사
    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            return true;
        } catch (err) {
            console.error('클립보드 복사 실패:', err);
            return false;
        }
    }
};

// Expose to global
window.Utils = Utils;
window.toastHandler = toastHandler;
