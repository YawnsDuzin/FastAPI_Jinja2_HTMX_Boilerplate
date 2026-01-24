/**
 * Main Application JavaScript
 *
 * HTMX와 Alpine.js를 사용하므로 최소한의 JavaScript만 포함합니다.
 */

// Toast Handler (Alpine.js component)
// 전역으로 정의하여 hx-boost 후에도 사용 가능
window.toastHandler = function toastHandler() {
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
};

// Alpine.js 재초기화 함수
function reinitializeAlpine(target) {
    if (typeof Alpine !== 'undefined' && Alpine.initTree) {
        // DOM이 완전히 업데이트된 후 Alpine 초기화
        requestAnimationFrame(() => {
            try {
                Alpine.initTree(target || document.body);
            } catch (e) {
                console.warn('Alpine.initTree error:', e);
            }
        });
    }
}

// HTMX 이벤트 핸들러 등록 (한 번만 실행)
if (!window.__htmxHandlersRegistered) {
    window.__htmxHandlersRegistered = true;

    // HTMX 콘텐츠 교체 후 Alpine.js 재초기화
    // 여러 이벤트에서 처리하여 확실하게 초기화
    document.addEventListener('htmx:afterSwap', (event) => {
        reinitializeAlpine(event.detail.target);
    });

    document.addEventListener('htmx:afterSettle', (event) => {
        reinitializeAlpine(event.detail.target);
    });

    // htmx:load는 새 콘텐츠가 DOM에 추가될 때마다 발생
    document.addEventListener('htmx:load', (event) => {
        reinitializeAlpine(event.detail.elt);
    });

    // HTMX 에러 핸들링
    document.addEventListener('htmx:responseError', (event) => {
        console.error('HTMX Error:', event.detail);

        // 401 에러 시 로그인 페이지로 리다이렉트
        if (event.detail.xhr && event.detail.xhr.status === 401) {
            window.location.href = '/login';
        }

        // 토스트 메시지 표시
        const errorMessage = (event.detail.xhr && event.detail.xhr.responseText) || '오류가 발생했습니다.';
        if (typeof htmx !== 'undefined') {
            htmx.trigger('#toast-container', 'showToast', {
                type: 'error',
                message: errorMessage
            });
        }
    });

    // HTMX 요청 전처리
    document.addEventListener('htmx:configRequest', (event) => {
        // JSON 요청인 경우 Content-Type 설정
        if (event.detail.headers['Content-Type'] === undefined) {
            // form 데이터는 자동으로 처리됨
        }
    });

    // HX-Trigger 이벤트 처리
    document.addEventListener('htmx:afterRequest', (event) => {
        if (!event.detail.xhr) return;

        const triggerHeader = event.detail.xhr.getResponseHeader('HX-Trigger');
        if (triggerHeader) {
            try {
                const triggers = JSON.parse(triggerHeader);

                // showToast 트리거 처리
                if (triggers.showToast && typeof htmx !== 'undefined') {
                    htmx.trigger('#toast-container', 'showToast', triggers.showToast);
                }

                // closeModal 트리거 처리
                if (triggers.closeModal && typeof htmx !== 'undefined') {
                    htmx.trigger(document.body, 'closeModal');
                }

                // refreshList 트리거 처리
                if (triggers.refreshList && typeof htmx !== 'undefined') {
                    htmx.trigger('#items-list', 'refresh');
                }
            } catch (e) {
                // 단순 문자열 트리거 - 무시
            }
        }
    });
}

// Dark mode initialization
(function () {
    // 시스템 설정 확인
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const storedMode = localStorage.getItem('darkMode');

    if (storedMode === 'true' || (storedMode === null && prefersDark)) {
        document.documentElement.classList.add('dark');
    }
})();

// 모달 닫기 함수 (전역)
// Alpine.js 커스텀 이벤트를 window 레벨에서 dispatch
// base.html의 @closeModal.window="open = false"가 이를 수신
window.closeModal = function() {
    window.dispatchEvent(new CustomEvent('closeModal'));
};

// Utility functions
window.Utils = {
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
